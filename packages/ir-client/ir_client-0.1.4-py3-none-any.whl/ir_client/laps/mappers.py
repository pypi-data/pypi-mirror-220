from ir_client.exceptions import MappingException
from ir_client.laps.models import Laps, Lap, LapEvent
from ir_client.utils.enum_utils import IntEnumSet


def map_laps(data) -> Laps:
    try:
        laps_data = data['lapData']
        return Laps(
            laps=[map_lap(lap) for lap in laps_data]
        )
    except KeyError:
        raise InvalidLapDataException(data)


def map_lap(lap_data) -> Lap:
    return Lap(
        number=lap_data['lap_num'],
        driver_id=lap_data['custid'],
        session_time_eol=lap_data['ses_time'],
        lap_events=IntEnumSet(LapEvent, lap_data['flags'])
    )


class InvalidLapDataException(MappingException):
    def __init__(self, data):
        pass
