"""
irclient library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

irclient is a library to retrieve data from the iRacing API.

Pull subsession results:
    >>> import irclient
    >>> endpoint_parameters = irclient.GetSubsessionResultsParameters(123456)
    >>> session_parameters = irclient.SessionParameters('some_cookie')
    >>> client = irclient.IracingClient()
    >>> client.get_data(
    ...     irclient.GetSubsessionResults,
    ...     endpoint_parameters,
    ...     session_parameters)
"""

from .iracing_client import IracingClient

from .session_parameters import SessionParameters

from .endpoint_parameters import GetSubsessionResultsParameters
from .endpoint_parameters import GetLapsParameters
from .endpoint_parameters import GetSeriesRaceResultsParameters

from .endpoint_types import GetSubsessionResults
from .endpoint_types import GetLaps
from .endpoint_types import GetSeriesRaceResults

from .subsession_results.models import SimSession, SimSessionType
from .laps.models import LapEvent, Lap
from .series_race_results.models import SeriesRaceResult
