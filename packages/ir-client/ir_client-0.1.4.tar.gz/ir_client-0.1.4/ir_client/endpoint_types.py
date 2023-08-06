from ir_client.series_race_results.mappers import map_series_race_results
from ir_client.subsession_results.mappers import map_subsession_results
from ir_client.laps.mappers import map_laps
from ir_client.utils.url_utils import build_relative_url, UrlWrapper

MEMBERSITE_PATH = build_relative_url("membersite", "member")
MEMBERSTATS_PATH = build_relative_url("memberstats", "member")


class Endpoint:
    def __init__(self, path, resource):
        self.path = path
        self.resource = resource


class EndpointType:
    def __init__(self, endpoint, mapper):
        self.endpoint = endpoint
        self.mapper = mapper

    def url(self, base_url: UrlWrapper):
        return base_url.resolve(self.endpoint.path).resolve(self.endpoint.resource)

    def map_data(self, data):
        return self.mapper(data)


class GetSubsessionResults(EndpointType):
    def __init__(self):
        # TODO improve 2nd parameter
        endpoint = Endpoint(MEMBERSITE_PATH, build_relative_url(leaf="GetSubsessionResults"))
        mapper = map_subsession_results
        super().__init__(endpoint, mapper)


class GetLaps(EndpointType):
    def __init__(self):
        # TODO improve 2nd parameter
        endpoint = Endpoint(MEMBERSITE_PATH, build_relative_url(leaf="GetLaps"))
        mapper = map_laps
        super().__init__(endpoint, mapper)


class GetSeriesRaceResults(EndpointType):
    def __init__(self):
        # TODO improve 2nd parameter
        endpoint = Endpoint(MEMBERSTATS_PATH, build_relative_url(leaf="GetSeriesRaceResults"))
        mapper = map_series_race_results
        super().__init__(endpoint, mapper)
