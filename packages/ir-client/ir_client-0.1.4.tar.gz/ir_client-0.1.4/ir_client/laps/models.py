from dataclasses import dataclass
from enum import IntEnum, unique

from ir_client.utils.enum_utils import IntEnumSet


@unique
class LapEvent(IntEnum):
    INVALID = 0
    PITTED = 1
    OFFTRACK = 2
    BLACK_FLAG = 3
    CAR_RESET = 4
    CONTACT = 5
    CAR_CONTACT = 6
    LOST_CONTROL = 7
    DISCONTINUITY = 8
    INTERPOLATED_CROSSING = 9
    CLOCK_SMASH = 10
    TOW = 11
    UNKNOWN_POSSIBLY_START_FROM_PITLANE = 12
    OPENING_LAP = 13
    FINAL_LAP = 14

    def as_binary(self):
        return 1 << self.value


@dataclass
class Lap:
    number: int
    driver_id: int
    session_time_eol: int
    lap_events: IntEnumSet


@dataclass
class Laps:
    laps: list[Lap]
