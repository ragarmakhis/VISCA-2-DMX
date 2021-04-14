"""Module for DMX universe."""
from typing import List, Set

from dmx.constants import DMX_MAX_ADDRESS
from dmx.unit import DMXUnit


class DMXUniverse:
    """Represents a DMX universe."""

    def __init__(self, universe_id: int = 1):
        """Initialise the DMX universe."""
        self._units = set()  # type: Set[DMXUnit]
        self._id = universe_id

    def add_unit(self, unit: DMXUnit):
        """Add a light to the universe."""
        self._units.add(unit)

    def remove_unit(self, unit: DMXUnit):
        """Remove a light from the universe."""
        self._units.remove(unit)

    def has_unit(self, unit: DMXUnit) -> bool:
        """Check if the universe has a light."""
        return unit in self._units

    def get_units(self) -> Set[DMXUnit]:
        """Get all lights in this universe."""
        return self._units

    def serialise(self) -> List[int]:
        """Serialise all the content of the DMX universe.

        Creates a frame which will update all lights to their current state.
        """
        frame = [0] * DMX_MAX_ADDRESS
        for unit in self._units:
            serialised_unit = unit.serialise()
            for address in range(unit.start_address, unit.end_address + 1):
                frame[address - 1] |= serialised_unit[address - unit.start_address]
        return frame
