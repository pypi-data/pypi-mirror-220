from datetime import timedelta

import pytest

from hukudo.gitlab.api import Gitlab
from hukudo.gitlab.jobs import get_duration, JobDurationParseError


@pytest.fixture
def gitlab():
    """
    For this fixture to work, you need a `~/.python-gitlab.cfg` containing something like this:

        [global]
        default = hukudo
        ssl_verify = true
        timeout = 30

        [hukudo]
        url = https://git.example.com/
        private_token = xxxxxxxxxxxxxxxxxxxx
        api_version = 4
    """
    return Gitlab.from_ini('hukudo')


def test_version(gitlab):
    actual = gitlab.version()
    major, minor, patch = [int(x) for x in actual.split('.')]
    assert major >= 16
    assert minor >= 1
    assert patch >= 1


def test_job_with_duration_happy():
    assert get_duration(
        {
            'started_at': '2022-07-19T16:13:17.374+02:00',
            'finished_at': '2022-07-19T16:14:19.374+02:00',
        }
    ) == timedelta(seconds=62)


def test_job_with_duration_error():
    with pytest.raises(JobDurationParseError):
        get_duration(
            {
                'started_at': 'not-an-iso-datetime-string',
                'finished_at': 'not-an-iso-datetime-string',
            }
        )
