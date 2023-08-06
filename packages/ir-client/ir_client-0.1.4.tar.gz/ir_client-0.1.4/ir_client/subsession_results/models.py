from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import auto

from typing import List, Dict

from ir_client.utils.enum_utils import AutoNameEnum


class SimSessionType(AutoNameEnum):
    PRACTICE = auto()
    QUALIFY = auto()
    WARMUP = auto()
    HEAT1 = auto()
    FEATURE = auto()
    RACE = auto()


@dataclass
class SimSessionEntry(ABC):
    """Abstract dataclass to provide general data on entries, that are not linked to a specific team or driver."""
    entry_id: int
    entry_name: str
    car_class_id: int
    car_class_name: str
    car_id: int
    car_name: str
    finish_position: int
    finish_position_class: int
    best_lap_time: int


@dataclass
class SimSessionDriverEntry(SimSessionEntry):
    is_team = False #TODO https://stackoverflow.com/questions/59904631/python-class-constants-in-dataclasses
    old_irating: int
    new_irating: int


@dataclass
class SimSessionTeamEntry(SimSessionEntry):
    is_team = True #TODO https://stackoverflow.com/questions/59904631/python-class-constants-in-dataclasses
    drivers: List[SimSessionDriverEntry] = field(default_factory=list)


@dataclass
class SimSession:
    number: int
    entries: List[SimSessionEntry]


@dataclass
class SubsessionResults:
    subsession_id: int
    start_time: datetime
    simulated_start_time: datetime
    team_session: bool
    sim_session_results: Dict[SimSessionType, SimSession]
