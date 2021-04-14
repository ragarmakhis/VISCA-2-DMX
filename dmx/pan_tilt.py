"""Module for DMX Pan/Tilt."""

from typing import List, Union


class PanTilt:
    """Represents a direction in 0-65535."""

    def __init__(self, pan_tilt: int):
        """Initialise the pan/tilt."""
        self.pan_tilt = pan_tilt

    def serialise(self) -> List[int]:
        """Serialise the direction order to a sequence of bytes."""
        return [self._pan_tilt / 256, self._pan_tilt % 256]

    @property
    def pan_tilt(self) -> int:
        """Get direction."""
        return self._pan_tilt

    @pan_tilt.setter
    def pan_tilt(self, value: int):
        """Set direction."""
        self._pan_tilt = int(max(0, min(value, 65535)))

    def __add__(self, other: Union['PanTilt', int, float]):
        """Handle add."""
        if isinstance(other, PanTilt):
            return PanTilt(self.pan_tilt + other.pan_tilt)
        elif isinstance(other, (int, float)):
            return PanTilt(int(self.pan_tilt + other))

    def __sub__(self, other: Union['PanTilt', int, float]):
        """Handle subtract."""
        if isinstance(other, PanTilt):
            return PanTilt(self.pan_tilt - other.pan_tilt)
        elif isinstance(other, (int, float)):
            return PanTilt(int(self.pan_tilt - other))

    def __mul__(self, other: Union['PanTilt', int, float]):
        """Handle multiply."""
        if isinstance(other, PanTilt):
            return PanTilt(self.pan_tilt * other.pan_tilt)
        elif isinstance(other, (int, float)):
            return PanTilt(int(self.pan_tilt * other))

    def __truediv__(self, other: Union['PanTilt', int, float]):
        """Handle division."""
        if isinstance(other, PanTilt):
            return PanTilt(int(self.pan_tilt / other.pan_tilt))
        elif isinstance(other, (int, float)):
            return PanTilt(int(self.pan_tilt / other))

    def __floordiv__(self, other: Union['PanTilt', int, float]):
        """Handle floor division."""
        if isinstance(other, PanTilt):
            return PanTilt(self.pan_tilt // other.pan_tilt)
        elif isinstance(other, (int, float)):
            return PanTilt(int(self.pan_tilt // other))
