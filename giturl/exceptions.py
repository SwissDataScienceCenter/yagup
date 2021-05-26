import attr


@attr.s
class InvalidURL(Exception):
    url = attr.ib()
