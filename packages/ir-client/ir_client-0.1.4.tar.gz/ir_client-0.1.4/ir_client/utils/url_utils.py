class UrlWrapper:
    def __init__(self, root_path, sub_path=None):
        self.root_path = root_path
        self.sub_path = sub_path

    def resolve(self, sub_path):
        return UrlWrapper(self, sub_path.root_path)

    def __str__(self):
        return '{0}{1}'.format(
            str(self.root_path),
            '' if self.sub_path is None else str(self.sub_path)[1:])


class RelativeUrlPath:
    def __init__(self, fragments=None, leaf=None):
        if fragments is None:
            fragments = []
        self.fragments = fragments
        self.leaf = leaf

    def __str__(self):
        return '{0}{1}/{2}'.format(
            '/' if self.fragments else '',
            '/'.join(self.fragments),
            self.leaf or '')


class AbsoluteUrlPath(RelativeUrlPath):
    def __init__(self, protocol, host, fragments=None, leaf=None):
        if fragments is None:
            fragments = []
        self.protocol = protocol
        self.host = host
        super().__init__(fragments, leaf)

    def __str__(self):
        return '{protocol}://{host}{fragments}'.format(
            protocol=self.protocol,
            host=self.host,
            fragments=super().__str__())


def build_absolute_url(protocol, host, *args, **kwargs):
    leaf = kwargs['leaf'] if 'leaf' in kwargs else None
    return UrlWrapper(AbsoluteUrlPath(protocol, host, list(args), leaf))


def build_relative_url(*args, **kwargs):
    leaf = kwargs['leaf'] if 'leaf' in kwargs else None
    return UrlWrapper(RelativeUrlPath(list(args), leaf))


