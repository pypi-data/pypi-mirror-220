from .control import *
from .tidal_euclid import *
from .pattern import *
from .utils import *
from .mini import *
from .stream import TidalStream

__streams = {}


def tidal_factory(env, osc_client, tidal_players):
    """Returns a tidal function to play Tidal patterns on a given OSC client"""
    env = env

    def tidal(key, pattern=None, data_only: bool = False):
        if key not in __streams:
            __streams[key] = TidalStream(
                data_only=data_only,
                name=key,
                osc_client=osc_client,
            )
            tidal_players.append(__streams[key])
        if pattern:
            __streams[key].pattern = pattern
        return __streams[key]

    return tidal


def hush_factory(env, osc_client, tidal_players):
    def hush():
        for stream in __streams.values():
            stream.pattern = silence
            tidal_players.remove(stream)
        __streams.clear()

    return hush


class __Streams:
    def __setitem__(self, key, value):
        p(key, value)


d = __Streams()
