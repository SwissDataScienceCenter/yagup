from pyparsing import (
    CaselessKeyword,
    Combine,
    Keyword,
    LineEnd,
    LineStart,
    Literal,
    NotAny,
    Optional,
    Word,
    ZeroOrMore,
    alphanums,
    nums,
    pyparsing_common,
)


def set_default_scheme(toks):
    if "scheme" not in toks:
        toks["scheme"] = "ssh"
    return toks


def scheme(s):
    return (
        CaselessKeyword(s)
        .setParseAction(pyparsing_common.downcaseTokens)
        .setResultsName("scheme")
    )


PART = Word(alphanums)
LABEL = PART + ZeroOrMore("-" + PART)
HOSTNAME = LABEL + ZeroOrMore("." + LABEL)
HOST = (
    Combine(HOSTNAME)
    .setParseAction(pyparsing_common.downcaseTokens)
    .setResultsName("host")
)
PORT = Word(nums).setParseAction(lambda toks: int(toks[0])).setResultsName("port")
USER = Word(alphanums, alphanums + "_-").setResultsName("user")
PATH = Word(alphanums + "+,/._-~").setResultsName("path")

LOCAL_URL = ((Keyword("file").setResultsName("scheme") + "://") | "/") + PATH

HTTP_URL = (
    (scheme("http") | scheme("https")).setResultsName("scheme")
    + "://"
    + Optional(USER + Literal("@"))
    + HOST
    + Optional(Literal(":") + PORT)
    + "/"
    + PATH
)

SSH_URL = (
    scheme("ssh")
    + "://"
    + Optional(USER + "@")
    + HOST
    + Optional(Literal(":") + PORT)
    + Literal("/")
    + PATH
)
SCP_LIKE_SSH_URL = (
    Optional(USER + "@") + HOST + NotAny(Literal("://")) + Literal(":") + PATH
).setParseAction(set_default_scheme)
GIT_URL = (
    scheme("git")
    + "://"
    + Optional(USER + "@")
    + HOST
    + Optional(Literal(":") + PORT)
    + Literal("/")
    + PATH
)
URL = (
    LineStart()
    + (HTTP_URL | SSH_URL | GIT_URL | SCP_LIKE_SSH_URL | LOCAL_URL)
    + LineEnd()
)
