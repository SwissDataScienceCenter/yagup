import pytest

from yagup import GitURL, InvalidURL


TESTDATA_GITURL_VALID = [
    (
        "https://github.com/kinkerl/glowing-octo-succotash.git",
        GitURL(
            scheme="https",
            host="github.com",
            path="kinkerl/glowing-octo-succotash.git",
        ),
    ),
    (
        "https://git@github.com/kinkerl/glowing-octo-succotash.git",
        GitURL(
            scheme="https",
            user="git",
            host="github.com",
            path="kinkerl/glowing-octo-succotash.git",
        ),
    ),
    (
        "https://git@github.com:8443/kinkerl/glowing-octo-succotash.git",
        GitURL(
            scheme="https",
            user="git",
            host="github.com",
            path="kinkerl/glowing-octo-succotash.git",
            port=8443,
        ),
    ),
    (
        "http://github.com/kinkerl/glowing-octo-succotash.git",
        GitURL(
            scheme="http", host="github.com", path="kinkerl/glowing-octo-succotash.git",
        ),
    ),
    (
        "git://github.com/kinkerl/glowing-octo-succotash.git",
        GitURL(
            scheme="git", host="github.com", path="kinkerl/glowing-octo-succotash.git",
        ),
    ),
    (
        "git://git.divio.com/ci-test-project-do-not-delete.git",
        GitURL(
            scheme="git",
            host="git.divio.com",
            path="ci-test-project-do-not-delete.git",
        ),
    ),
    (
        "ssh://github.com/kinkerl/glowing-octo-succotash.git",
        GitURL(
            scheme="ssh", host="github.com", path="kinkerl/glowing-octo-succotash.git",
        ),
    ),
    (
        "ssh://git@github.com/kinkerl/glowing-octo-succotash.git",
        GitURL(
            scheme="ssh",
            user="git",
            host="github.com",
            path="kinkerl/glowing-octo-succotash.git",
        ),
    ),
    (
        "ssh://git.divio.com/ci-test-project-do-not-delete.git",
        GitURL(
            scheme="ssh",
            host="git.divio.com",
            path="ci-test-project-do-not-delete.git",
        ),
    ),
    (
        "ssh://git.divio.com:2222/ci-test-project-do-not-delete.git",
        GitURL(
            scheme="ssh",
            host="git.divio.com",
            path="ci-test-project-do-not-delete.git",
            port=2222,
        ),
    ),
    (
        "SSH://GIT.divio.com:2222/ci-test-project-do-not-delete.git",
        GitURL(
            scheme="ssh",
            host="git.divio.com",
            path="ci-test-project-do-not-delete.git",
            port=2222,
        ),
    ),
    (
        "git@github.com:vxsx/animated-octo-doodle.git",
        GitURL(
            scheme="ssh",
            user="git",
            host="github.com",
            path="vxsx/animated-octo-doodle.git",
        ),
    ),
    ("file:///tmp/test.git", GitURL(scheme="file", path="/tmp/test.git",),),
]
TESTDATA_GITURL_INVALID = [
    # Invalid scheme
    "nothing://github.com/kinkerl/glowing-octo-succotash.git",
    # : is not correct
    "ssh://github.com:kinkerl/glowing-octo-succotash.git",
    # : is not correct
    "git://github.com:kinkerl/glowing-octo-succotash.git",
    # Spaces
    "git@github.com:vxsx/animated-octo-d oodle.git",
    " git@github.com:vxsx/animated-octo-d oodle.git",
    "git@github.com:vxsx/animated-octo-d oodle.git ",
    "git @github.com:vxsx/animated-octo-d oodle.git",
    "git@github.co m:vxsx/animated-octo-d oodle.git",
    "git@github.com:vxsx/ animated-octo-d oodle.git",
    "",
    " ",
    "ssh://",
    "ssh://a",
]

TESTDATA_GITURL_NORMALIZE = [
    (
        "https://github.com/kinkerl/glowing-octo-succotash.git",
        "https://github.com/kinkerl/glowing-octo-succotash.git",
    ),
    (
        "git://github.com/kinkerl/glowing-octo-succotash.git",
        "git://github.com/kinkerl/glowing-octo-succotash.git",
    ),
    (
        "git@github.com:kinkerl/glowing-octo-succotash.git",
        "ssh://git@github.com/kinkerl/glowing-octo-succotash.git",
    ),
    (
        "git://git.divio.com/ci-test-project-do-not-delete.git",
        "git://git.divio.com/ci-test-project-do-not-delete.git",
    ),
    (
        "ssh://github.com/kinkerl/glowing-octo-succotash.git",
        "ssh://github.com/kinkerl/glowing-octo-succotash.git",
    ),
    (
        "ssh://git.divio.com/ci-test-project-do-not-delete.git",
        "ssh://git.divio.com/ci-test-project-do-not-delete.git",
    ),
    (
        "ssh://git.DiVIO.com/ci-test-project-do-not-delete.git",
        "ssh://git.divio.com/ci-test-project-do-not-delete.git",
    ),
    (
        "SSH://git.DiVIO.com/ci-test-project-do-not-delete.git",
        "ssh://git.divio.com/ci-test-project-do-not-delete.git",
    ),
]


@pytest.mark.parametrize("url,expected", TESTDATA_GITURL_VALID)
def test_parse_valid(url, expected):
    parsed = GitURL.parse(url)
    assert parsed == expected


@pytest.mark.parametrize("url", TESTDATA_GITURL_INVALID)
def test_parse_invalid(url):
    with pytest.raises(InvalidURL):
        GitURL.parse(url)


# url styles we do not support
@pytest.mark.parametrize("url,expected", TESTDATA_GITURL_NORMALIZE)
def test_normalize(url, expected):
    assert str(GitURL.parse(url)) == expected
