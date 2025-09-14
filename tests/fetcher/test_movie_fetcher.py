from unittest import mock

import pytest

from client_app_cli.auth.authenticator import Authenticator
from client_app_cli.constants.constant import (
    DEFAULT_USERNAME,
    DEFAULT_PASSWORD,
    BASE_URL,
)
from client_app_cli.fetcher.movie_fetcher import MovieFetcher
from tests.mocks import (
    mocked_auth_failure,
    mocked_fetch_success,
    mocked_auth_success,
    mocked_fetch_failure,
)


@pytest.fixture
def authenticator():
    """
    returns Authenticator instance to use in movie fetcher
    """
    return Authenticator(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)


@pytest.fixture()
def years():
    """
    returns a list of years
    """
    return ["1940", "1950"]


@pytest.fixture()
def fetcher(authenticator, years):
    """
    returns a MovieFetcher instance using authenticator instance and years list
    """
    return MovieFetcher(years, authenticator)


@mock.patch("requests.post", side_effect=mocked_auth_failure)
def test_auth_failure(mock_post, fetcher):
    """
    Test that unsuccessful authentication returns None for the specified year
    :param mock_post: mocks the response of the requests.post
    """
    assert fetcher.fetch_movies()["1940"] is None


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_success)
def test_fetch_success(mock_post, mock_get, fetcher):
    """
    Test that successful fetching returns a dictionary and the correct number of movies for a given year
    :param mock_post:
    :param mock_get: mocks the response of the requests.get
    :param fetcher: fetcher instance
    """
    fetch_response = fetcher.fetch_movies()
    assert type(fetch_response) is dict
    assert fetch_response["1940"] == 2
    assert fetch_response["1950"] == 2


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_failure)
def test_fetch_failure(mock_post, mock_get, fetcher):
    """
    Test that unsuccessful fetching returns a dictionary with None for the specified year
    :param mock_post:
    :param mock_get:
    :param fetcher:
    :return:
    """
    assert fetcher.fetch_movies()["1940"] is None
