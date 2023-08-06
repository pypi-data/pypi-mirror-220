from dataclasses import dataclass


# TODO class BodyParameter:
# TODO     def __init__(self, key):
# TODO         self.key = key


@dataclass
class GetSubsessionResultsParameters:
    subsession_id: int

    # TODO find a way to generate this automatically
    def as_dict(self):
        return {
            'subsessionID': self.subsession_id,
        }


@dataclass
class GetLapsParameters:
    # TODO idea subsession_id = BodyParameter('subsessionid')
    # TODO idea group_id = BodyParameter('groupid')
    # TODO idea customer_id = BodyParameter('custid')
    # TODO idea sim_session_number = BodyParameter('simsesnum')

    subsession_id: int
    sim_session_number: int
    group_id: int
    customer_id: int = None

    def as_dict(self):
        return {
            'subsessionid': self.subsession_id,
            'groupid': self.group_id,
            'custid': self.customer_id,
            'simsesnum': self.sim_session_number
        }


@dataclass
class GetSeriesRaceResultsParameters:
    season_id: int
    raceweek: int

    def as_dict(self):
        return {
            'seasonid': self.season_id,
            'raceweek': self.raceweek
        }
