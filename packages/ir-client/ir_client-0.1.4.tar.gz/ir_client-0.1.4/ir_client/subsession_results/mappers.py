from typing import Dict, List
from urllib.parse import unquote_plus

from ir_client.exceptions import MappingException
from ir_client.subsession_results.models import SimSessionEntry, SimSessionDriverEntry, SimSession
from ir_client.subsession_results.models import SimSessionTeamEntry
from ir_client.subsession_results.models import SimSessionType
from ir_client.subsession_results.models import SubsessionResults
from ir_client.utils import datetime_utils


def map_subsession_results(data) -> SubsessionResults:
    try:
        if isinstance(data, list):
            raise InvalidSubsessionResultsDataException() #TODO test
        is_team_session = bool(data['driver_changes'])
        return SubsessionResults(
            subsession_id=data['subsessionid'],
            start_time=datetime_utils.parse_datetime(unquote_plus(data['start_time'])),
            simulated_start_time=datetime_utils.parse_datetime_short(unquote_plus(data['simulatedstarttime'])),
            team_session=is_team_session,
            sim_session_results=map_sim_sessions(data['rows'], is_team_session)
        )
    except KeyError as e:
        raise InvalidSubsessionResultsDataException() from e


def map_sim_sessions(rows, is_team_session=False) -> Dict[SimSessionType, List[SimSessionEntry]]:
    if rows:
        sim_sessions = {}
        if is_team_session:
            tmp_sim_sessions = {}
            # TODO optimize
            for row in (r for r in rows if r['custid'] < 0):
                sim_session_type = __determine_sim_session_type(row)
                if sim_session_type not in tmp_sim_sessions:
                    tmp_sim_sessions[sim_session_type] = (row['simsesnum'], {})
                tmp_sim_sessions[sim_session_type][1][row['custid']] = map_sim_session_team_entry(row)
            for row in (r for r in rows if r['custid'] > 0):
                sim_session_type = __determine_sim_session_type(row)
                tmp_sim_sessions[sim_session_type][1][row['groupid']].drivers.append(map_sim_session_driver_entry(row))
            for x, y, z in ((x, y, z) for x, (y, d) in tmp_sim_sessions.items() for (_, z) in d.items()):
                if x is not None:
                    sim_session = __get_or_create_sim_session(sim_sessions, sim_session_type=x, sim_session_number=y)
                    sim_session.entries.append(z)
        else:
            for row in rows:
                sim_session = __get_or_create_sim_session(sim_sessions, row=row)
                if sim_session is not None:
                    sim_session.entries.append(map_sim_session_driver_entry(row))
        return sim_sessions
    return {}


def __get_or_create_sim_session(sim_sessions, row=None, sim_session_type=None, sim_session_number=None):
    # TODO verify params
    sim_session_type = sim_session_type or __determine_sim_session_type(row)
    sim_session_number = sim_session_number if sim_session_number is not None else row['simsesnum']
    if sim_session_type is not None and sim_session_type not in sim_sessions:
        sim_sessions[sim_session_type] = SimSession(
            number=sim_session_number,
            entries=[]  # TODO default parameter
        )
    return sim_sessions[sim_session_type] if sim_session_type is not None else None


def __determine_sim_session_type(row):
    if __is_race(row):
        return SimSessionType.RACE
    elif __is_qualifying(row):
        return SimSessionType.QUALIFY
    else:
        return None


def __is_race(row):
    return row['simsestypename'] == 'Race'


def __is_qualifying(row):
    return row['simsestypename'] in ['Open+Qualifying', 'Lone+Qualifying']


def map_sim_session_team_entry(row) -> SimSessionTeamEntry:
    return SimSessionTeamEntry(
        entry_id=row['custid'],
        entry_name=unquote_plus(row['displayname']),
        car_class_id=row['carclassid'],
        car_class_name=unquote_plus(row['ccName']),
        car_id=row['carid'],
        car_name=unquote_plus(row['car_name']), #TODO test
        finish_position=row['finishpos'],
        finish_position_class=row['finishposinclass'],
        best_lap_time=row['bestlaptime'],
    )


def map_sim_session_driver_entry(row) -> SimSessionDriverEntry:
    return SimSessionDriverEntry(
        entry_id=row['custid'],
        entry_name=unquote_plus(row['displayname']),
        car_class_id=row['carclassid'],
        car_class_name=unquote_plus(row['ccName']),
        car_id=row['carid'],
        car_name=unquote_plus(row['car_name']), #TODO test
        finish_position=row['finishpos'],
        finish_position_class=row['finishposinclass'],
        best_lap_time=row['bestlaptime'],
        old_irating=row['oldirating'],
        new_irating=row['newirating']
    )


class InvalidSubsessionResultsDataException(MappingException):
    pass
