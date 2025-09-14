from unittest import mock

import pytest

from client_app_cli.auth.authenticator import Authenticator
from client_app_cli.constants.constant import DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL
from client_app_cli.exceptions.exceptions import AuthenticationException
from client_app_cli.fetcher.movie_fetcher import MovieFetcher
from tests.mocks import mocked_failure, mocked_fetch_success, mocked_auth_success


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

@mock.patch("requests.post", side_effect=mocked_failure)
def test_auth_failure(mock_post, fetcher):
    """
    Test that unsuccessful authentication raises AuthenticationException when movie fetching
    :param mock_post: mocks the response of the requests.post
    """
    with pytest.raises(AuthenticationException, match=r".*invalid token*"):
        fetcher.fetch_movies()

@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_success)
def test_fetch_success(mock_post, mock_get, fetcher):
    """
    Test that successful fetching returns a dictionary and the correct number of movies for a given year
    :param mock_get:
    :param fetcher:
    :return:
    """
    fetch_response = fetcher.fetch_movies()
    assert type(fetch_response) is dict
    assert fetch_response["1940"] == 2
    assert fetch_response["1950"] == 2
