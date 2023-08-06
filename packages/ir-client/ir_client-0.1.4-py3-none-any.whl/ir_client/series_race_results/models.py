from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class SeriesRaceResult:
    subsession_id: int


@dataclass
class SeriesRaceResultsSlot:
    results: list[SeriesRaceResult] = field(default_factory=lambda: [])


@dataclass
class SeriesRaceResultCollection:
    slots: dict[datetime, SeriesRaceResultsSlot]
