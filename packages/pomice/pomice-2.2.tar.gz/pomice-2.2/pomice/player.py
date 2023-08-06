import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from discord import Client
from discord import Guild
from discord import VoiceChannel
from discord import VoiceProtocol
from discord.ext import commands
from discord.types.voice import GuildVoiceState
from discord.types.voice import VoiceServerUpdate

from . import events
from .enums import SearchType
from .events import PomiceEvent
from .events import TrackEndEvent
from .events import TrackStartEvent
from .exceptions import FilterInvalidArgument
from .exceptions import FilterTagAlreadyInUse
from .exceptions import FilterTagInvalid
from .exceptions import TrackInvalidPosition
from .exceptions import TrackLoadError
from .filters import Filter
from .objects import Playlist
from .objects import Track
from .pool import Node
from .pool import NodePool

__all__ = ("Filters", "Player")


class Filters:
    """Helper class for filters"""

    __slots__ = ("_filters",)

    def __init__(self) -> None:
        self._filters: List[Filter] = []

    @property
    def has_preload(self) -> bool:
        """Property which checks if any applied filters were preloaded"""
        return any(f for f in self._filters if f.preload == True)

    @property
    def has_global(self) -> bool:
        """Property which checks if any applied filters are global"""
        return any(f for f in self._filters if f.preload == False)

    @property
    def empty(self) -> bool:
        """Property which checks if the filter list is empty"""
        return len(self._filters) == 0

    def add_filter(self, *, filter: Filter) -> None:
        """Adds a filter to the list of filters applied"""
        if any(f for f in self._filters if f.tag == filter.tag):
            raise FilterTagAlreadyInUse(
                "A filter with that tag is already in use.",
            )
        self._filters.append(filter)

    def remove_filter(self, *, filter_tag: str) -> None:
        """Removes a filter from the list of filters applied using its filter tag"""
        if not any(f for f in self._filters if f.tag == filter_tag):
            raise FilterTagInvalid("A filter with that tag was not found.")

        for index, filter in enumerate(self._filters):
            if filter.tag == filter_tag:
                del self._filters[index]

    def has_filter(self, *, filter_tag: str) -> bool:
        """Checks if a filter exists in the list of filters using its filter tag"""
        return any(f for f in self._filters if f.tag == filter_tag)

    def reset_filters(self) -> None:
        """Removes all filters from the list"""
        self._filters = []

    def get_preload_filters(self) -> List[Filter]:
        """Get all preloaded filters"""
        return [f for f in self._filters if f.preload == True]

    def get_all_payloads(self) -> Dict[str, Any]:
        """Returns a formatted dict of all the filter payloads"""
        payload: Dict[str, Any] = {}
        for _filter in self._filters:
            if _filter.payload:
                payload.update(_filter.payload)
        return payload

    def get_filters(self) -> List[Filter]:
        """Returns the current list of applied filters"""
        return self._filters


class Player(VoiceProtocol):
    """The base player class for Pomice.
    In order to initiate a player, you must pass it in as a cls when you connect to a channel.
    i.e: ```py
    await ctx.author.voice.channel.connect(cls=pomice.Player)
    ```
    """

    __slots__ = (
        "client",
        "channel",
        "_bot",
        "_guild",
        "_node",
        "_current",
        "_filters",
        "_volume",
        "_paused",
        "_is_connected",
        "_position",
        "_last_position",
        "_last_update",
        "_ending_track",
        "_voice_state",
        "_player_endpoint_uri",
    )

    def __call__(self, client: Client, channel: VoiceChannel) -> "Player":
        self.__init__(client, channel)  # type: ignore
        return self

    def __init__(
        self,
        client: Client,
        channel: VoiceChannel,
        *,
        node: Optional[Node] = None,
    ) -> None:
        self.client: Client = client
        self.channel: VoiceChannel = channel

        self._bot: Client = client
        self._guild: Guild = channel.guild
        self._node: Node = node if node else NodePool.get_node()
        self._current: Optional[Track] = None
        self._filters: Filters = Filters()
        self._volume: int = 100
        self._paused: bool = False
        self._is_connected: bool = False

        self._position: int = 0
        self._last_position: int = 0
        self._last_update: float = 0
        self._ending_track: Optional[Track] = None

        self._voice_state: dict = {}

        self._player_endpoint_uri: str = f"sessions/{self._node._session_id}/players"

    def __repr__(self) -> str:
        return (
            f"<Pomice.player bot={self.bot} guildId={self.guild.id} "
            f"is_connected={self.is_connected} is_playing={self.is_playing}>"
        )

    @property
    def position(self) -> float:
        """Property which returns the player's position in a track in milliseconds"""
        if not self.is_playing or not self._current:
            return 0

        current = getattr(self._current, "original", self._current)

        if self.is_paused:
            return min(self._last_position, current.length)

        difference = (time.time() * 1000) - self._last_update
        position = self._last_position + difference

        if position > current.length:
            return 0

        return min(position, current.length)

    @property
    def is_playing(self) -> bool:
        """Property which returns whether or not the player is actively playing a track."""
        return self._is_connected and self._current is not None

    @property
    def is_connected(self) -> bool:
        """Property which returns whether or not the player is connected"""
        return self._is_connected

    @property
    def is_paused(self) -> bool:
        """Property which returns whether or not the player has a track which is paused or not."""
        return self._is_connected and self._paused

    @property
    def current(self) -> Optional[Track]:
        """Property which returns the currently playing track"""
        return self._current

    @property
    def node(self) -> Node:
        """Property which returns the node the player is connected to"""
        return self._node

    @property
    def guild(self) -> Guild:
        """Property which returns the guild associated with the player"""
        return self._guild

    @property
    def volume(self) -> int:
        """Property which returns the players current volume"""
        return self._volume

    @property
    def filters(self) -> Filters:
        """Property which returns the helper class for interacting with filters"""
        return self._filters

    @property
    def bot(self) -> Client:
        """Property which returns the bot associated with this player instance"""
        return self._bot

    @property
    def is_dead(self) -> bool:
        """Returns a bool representing whether the player is dead or not.
        A player is considered dead if it has been destroyed and removed from stored players.
        """
        return self.guild.id not in self._node._players

    async def _update_state(self, data: dict) -> None:
        state: dict = data.get("state", {})
        self._last_update = time.time() * 1000.0
        self._is_connected = bool(state.get("connected"))
        position = state.get("position")
        self._last_position = int(position) if position else 0

    async def _dispatch_voice_update(self, voice_data: Optional[Dict[str, Any]] = None) -> None:
        if {"sessionId", "event"} != self._voice_state.keys():
            return

        state = voice_data or self._voice_state

        data = {
            "token": state["event"]["token"],
            "endpoint": state["event"]["endpoint"],
            "sessionId": state["sessionId"],
        }

        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data={"voice": data},
        )

    async def on_voice_server_update(self, data: VoiceServerUpdate) -> None:
        self._voice_state.update({"event": data})
        await self._dispatch_voice_update(self._voice_state)

    async def on_voice_state_update(self, data: GuildVoiceState) -> None:
        self._voice_state.update({"sessionId": data.get("session_id")})

        channel_id = data.get("channel_id")
        if not channel_id:
            await self.disconnect()
            self._voice_state.clear()
            return

        channel = self.guild.get_channel(int(channel_id))
        if not channel:
            await self.disconnect()
            self._voice_state.clear()
            return

        if not data.get("token"):
            return

        await self._dispatch_voice_update({**self._voice_state, "event": data})

    async def _dispatch_event(self, data: dict) -> None:
        event_type: str = data["type"]
        event: PomiceEvent = getattr(events, event_type)(data, self)

        if isinstance(event, TrackEndEvent) and event.reason != "REPLACED":
            self._current = None

        event.dispatch(self._bot)

        if isinstance(event, TrackStartEvent):
            self._ending_track = self._current

    async def _swap_node(self, *, new_node: Node) -> None:
        data: dict = {
            "position": self.position,
        }
        if self.current:
            data["encodedTrack"] = self.current.track_id

        del self._node._players[self._guild.id]
        self._node = new_node
        self._node._players[self._guild.id] = self
        # reassign uri to update session id
        self._player_endpoint_uri = f"sessions/{self._node._session_id}/players"

        await self._dispatch_voice_update()
        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data=data,
        )

    async def get_tracks(
        self,
        query: str,
        *,
        ctx: Optional[commands.Context] = None,
        search_type: SearchType = SearchType.ytsearch,
        filters: Optional[List[Filter]] = None,
    ) -> Optional[Union[List[Track], Playlist]]:
        """Fetches tracks from the node's REST api to parse into Lavalink.

        If you passed in Spotify API credentials when you created the node,
        you can also pass in a Spotify URL of a playlist, album or track and it will be parsed
        accordingly.

        You can pass in a discord.py Context object to get a
        Context object on any track you search.

        You may also pass in a List of filters
        to be applied to your track once it plays.
        """
        return await self._node.get_tracks(query, ctx=ctx, search_type=search_type, filters=filters)

    async def get_recommendations(
        self, *, track: Track, ctx: Optional[commands.Context] = None
    ) -> Optional[Union[List[Track], Playlist]]:
        """
        Gets recommendations from either YouTube or Spotify.
        You can pass in a discord.py Context object to get a
        Context object on all tracks that get recommended.
        """
        return await self._node.get_recommendations(track=track, ctx=ctx)

    async def connect(
        self, *, timeout: float, reconnect: bool, self_deaf: bool = False, self_mute: bool = False
    ) -> None:
        await self.guild.change_voice_state(
            channel=self.channel,
            self_deaf=self_deaf,
            self_mute=self_mute,
        )
        self._node._players[self.guild.id] = self
        self._is_connected = True

    async def stop(self) -> None:
        """Stops the currently playing track."""
        self._current = None
        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data={"encodedTrack": None},
        )

    async def disconnect(self, *, force: bool = False) -> None:
        """Disconnects the player from voice."""
        try:
            await self.guild.change_voice_state(channel=None)
        finally:
            self.cleanup()
            self._is_connected = False
            del self.channel

    async def destroy(self) -> None:
        """Disconnects and destroys the player, and runs internal cleanup."""
        try:
            await self.disconnect()
        except AttributeError:
            # 'NoneType' has no attribute '_get_voice_client_key' raised by self.cleanup() ->
            # assume we're already disconnected and cleaned up
            assert not self.is_connected and not self.channel

        self._node._players.pop(self.guild.id)
        await self._node.send(
            method="DELETE",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
        )

    async def play(
        self, track: Track, *, start: int = 0, end: int = 0, ignore_if_playing: bool = False
    ) -> Track:
        """Plays a track. If a Spotify track is passed in, it will be handled accordingly."""

        # Make sure we've never searched the track before
        if track.original is None:
            # First lets try using the tracks ISRC, every track has one (hopefully)
            try:
                if not track.isrc:
                    # We have to bare raise here because theres no other way to skip this block feasibly
                    raise
                search = (
                    await self._node.get_tracks(f"{track._search_type}:{track.isrc}", ctx=track.ctx)
                )[
                    0
                ]  # type: ignore
            except Exception:
                # First method didn't work, lets try just searching it up
                try:
                    search = (
                        await self._node.get_tracks(
                            f"{track._search_type}:{track.title} - {track.author}",
                            ctx=track.ctx,
                        )
                    )[
                        0
                    ]  # type: ignore
                except:
                    # The song wasn't able to be found, raise error
                    raise TrackLoadError(
                        "No equivalent track was able to be found.",
                    )
            data = {
                "encodedTrack": search.track_id,
                "position": str(start),
                "endTime": str(track.length),
            }
            track.original = search
            track.track_id = search.track_id
            # Set track_id for later lavalink searches
        else:
            data = {
                "encodedTrack": track.track_id,
                "position": str(start),
                "endTime": str(track.length),
            }

        # Lets set the current track before we play it so any
        # corresponding events can capture it correctly

        self._current = track

        # Remove preloaded filters if last track had any
        if self.filters.has_preload:
            for filter in self.filters.get_preload_filters():
                await self.remove_filter(filter_tag=filter.tag)

        # Global filters take precedence over track filters
        # So if no global filters are detected, lets apply any
        # necessary track filters

        # Check if theres no global filters and if the track has any filters
        # that need to be applied

        if track.filters and not self.filters.has_global:
            # Now apply all filters
            for filter in track.filters:
                await self.add_filter(_filter=filter)

        # Lavalink v4 changed the way the end time parameter works
        # so now the end time cannot be zero.
        # If it isnt zero, it'll match the length of the track,
        # otherwise itll be set here:

        if end > 0:
            data["endTime"] = str(end)

        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data=data,
            query=f"noReplace={ignore_if_playing}",
        )

        return self._current

    async def seek(self, position: float) -> float:
        """Seeks to a position in the currently playing track milliseconds"""
        if not self._current or not self._current.original:
            return 0.0

        if position < 0 or position > self._current.original.length:
            raise TrackInvalidPosition(
                "Seek position must be between 0 and the track length",
            )

        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data={"position": position},
        )
        return self._position

    async def set_pause(self, pause: bool) -> bool:
        """Sets the pause state of the currently playing track."""
        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data={"paused": pause},
        )
        self._paused = pause
        return self._paused

    async def set_volume(self, volume: int) -> int:
        """Sets the volume of the player as an integer. Lavalink accepts values from 0 to 500."""
        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data={"volume": volume},
        )
        self._volume = volume
        return self._volume

    async def add_filter(self, _filter: Filter, fast_apply: bool = False) -> Filters:
        """Adds a filter to the player. Takes a pomice.Filter object.
        This will only work if you are using a version of Lavalink that supports filters.
        If you would like for the filter to apply instantly, set the `fast_apply` arg to `True`.

        (You must have a song playing in order for `fast_apply` to work.)
        """

        self._filters.add_filter(filter=_filter)
        payload = self._filters.get_all_payloads()
        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data={"filters": payload},
        )
        if fast_apply:
            await self.seek(self.position)

        return self._filters

    async def remove_filter(self, filter_tag: str, fast_apply: bool = False) -> Filters:
        """Removes a filter from the player. Takes a filter tag.
        This will only work if you are using a version of Lavalink that supports filters.
        If you would like for the filter to apply instantly, set the `fast_apply` arg to `True`.

        (You must have a song playing in order for `fast_apply` to work.)
        """

        self._filters.remove_filter(filter_tag=filter_tag)
        payload = self._filters.get_all_payloads()
        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data={"filters": payload},
        )
        if fast_apply:
            await self.seek(self.position)

        return self._filters

    async def reset_filters(self, *, fast_apply: bool = False) -> None:
        """Resets all currently applied filters to their default parameters.
         You must have filters applied in order for this to work.
         If you would like the filters to be removed instantly, set the `fast_apply` arg to `True`.

        (You must have a song playing in order for `fast_apply` to work.)
        """

        if not self._filters:
            raise FilterInvalidArgument(
                "You must have filters applied first in order to use this method.",
            )
        self._filters.reset_filters()
        await self._node.send(
            method="PATCH",
            path=self._player_endpoint_uri,
            guild_id=self._guild.id,
            data={"filters": {}},
        )

        if fast_apply:
            await self.seek(self.position)
