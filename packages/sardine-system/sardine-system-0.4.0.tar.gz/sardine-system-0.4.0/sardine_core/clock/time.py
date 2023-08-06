import contextlib
import contextvars

from ..base import BaseHandler

__all__ = ("Time",)

shift = contextvars.ContextVar("shift", default=0.0)
"""
This specifies the amount of time to offset in the current context.
Usually this is updated within the context of scheduled functions
to simulate sleeping without actually blocking the function. Behavior is
undefined if time is shifted in the global context.
"""


class Time(BaseHandler):
    """Contains the origin of a FishBowl's time.

    Any new clocks must continue from this origin when they are running,
    and must update the origin when they are paused or stopped.
    """

    def __init__(
        self,
        origin: float = 0.0,
    ):
        super().__init__()
        self._origin = origin

    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            " ".join(f"{attr}={getattr(self, attr)!r}" for attr in ("origin",)),
        )

    @property
    def origin(self) -> float:
        """The origin of the fish bowl's time.

        When this property is updated, an `origin_update` event
        will be dispatched with two arguments, the old and the new
        origin.
        """
        return self._origin

    @origin.setter
    def origin(self, new_origin: float):
        old_origin = self._origin
        self._origin = new_origin

        self.env.dispatch("origin_update", old_origin, new_origin)

    @property
    def shift(self) -> float:
        """The time shift in the current context.

        This is useful for simulating sleeps without blocking.
        """
        return shift.get()

    @shift.setter
    def shift(self, seconds: float):
        shift.set(seconds)

    @contextlib.contextmanager
    def scoped_shift(self, seconds: float):
        """Returns a context manager that adds `seconds` to the clock.

        After the context manager is exited, the time shift is restored
        to its previous value.
        """
        token = shift.set(shift.get() + seconds)
        try:
            yield
        finally:
            shift.reset(token)

    def reset(self):
        """Resets the time origin back to 0."""
        self._origin = 0.0
