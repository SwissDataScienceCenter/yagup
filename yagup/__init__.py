import attr
from pyparsing import ParseException

from .exceptions import InvalidURL
from .schema import URL

__author__ = "Swiss Data Science Center"
__email__ = "contact@datascience.ch"
__version__ = "0.1.0"
__url__ = "https://datascience.ch/"


@attr.s(frozen=True)
class GitURL:
    scheme = attr.ib(default=None)
    host = attr.ib(default=None)
    path = attr.ib(default=None)
    user = attr.ib(default=None)
    port = attr.ib(default=None)
    _parsing_result = attr.ib(default=None, cmp=False, repr=False)

    def __str__(self):
        authinfo = f"{self.user}@" if self.user else ""
        netloc = f"{self.host}:{self.port}" if self.port else self.host
        return f"{self.scheme}://{authinfo}{netloc}/{self.path}"

    @classmethod
    def parse(cls, url):
        try:
            res = URL.parseString(url, parseAll=True)
        except ParseException:
            raise InvalidURL(url)
        return GitURL(**res, parsing_result=res)


def parse(url):
    """
    Handy alias to
    """
    return GitURL.parse(url)
