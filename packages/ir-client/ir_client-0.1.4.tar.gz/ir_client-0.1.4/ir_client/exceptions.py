class IracingClientException(Exception):
    pass

class InvalidDataException(IracingClientException):
    def __init__(self, endpoint_type_cls, endpoint_parameters, content):
        pass


class AuthorizationFailedException(IracingClientException):
    pass


class MappingException(IracingClientException):
    pass
