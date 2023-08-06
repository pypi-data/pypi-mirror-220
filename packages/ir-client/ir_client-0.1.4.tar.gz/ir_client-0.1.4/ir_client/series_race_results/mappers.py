from typing import List
from ir_client.utils.collections import defaultordereddict #TODO extract different lib
from more_itertools import unique_everseen
from datetime import datetime, timezone

from ir_client.exceptions import MappingException
from ir_client.series_race_results.models import (
    SeriesRaceResult,
    SeriesRaceResultsSlot,
    SeriesRaceResultCollection
)

def map_series_race_results(data) -> SeriesRaceResultCollection:
    try:
        headers = {name: pos for (pos, name) in data['m'].items()}
        slots = defaultordereddict(lambda: SeriesRaceResultsSlot())
        races = _get_races(data, headers)
        for race in races:
            start_time = race[headers["start_time"]]
            dt_start_time = datetime.fromtimestamp(start_time / 1e3, tz=timezone.utc)
            slots[dt_start_time].results.append(_map_single_race(race, headers))
        return SeriesRaceResultCollection(slots=slots)
    except KeyError:
        raise InvalidSeriesRaceResultsDataException()

def _get_races(data, headers):
    return unique_everseen(
        data['d'],
        key=lambda r: r[headers['subsessionid']])


def _map_single_race(race, headers) -> SeriesRaceResult:
    return SeriesRaceResult(
        subsession_id=race[headers['subsessionid']]
    )


class InvalidSeriesRaceResultsDataException(MappingException):
    pass
