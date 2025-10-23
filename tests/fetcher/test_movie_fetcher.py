from unittest import mock

import pytest

from client_app_cli.arguments.arguments import Arguments
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
    mocked_fetch_auth_failure,
    mocked_fetch_failure,
    mocked_fetch_exception_failure,
    mocked_fetch_success_with_search_term,
    mocked_fetch_success_for_pages_more_than_100,
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
    return [1940, 1950]


@pytest.fixture()
def fetcher(authenticator):
    """
    returns a MovieFetcher instance using authenticator instance
    """
    return MovieFetcher(authenticator)


@mock.patch("requests.post", side_effect=mocked_auth_failure)
def test_auth_failure(mock_post, fetcher, years):
    """
    Test that unsuccessful authentication returns None for the specified year
    """
    args = Arguments(years, "", False)
    assert fetcher.fetch_movies(args)[1940] is None


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_success)
def test_fetch_success_without_search_term(mock_post, mock_get, fetcher, years):
    """
    Test that successful fetching returns a dictionary and the correct number of movies for a given year
    :param mock_post:
    :param mock_get: mocks the response of the requests.get
    :param fetcher: fetcher instance
    :param years: years instance
    """
    args = Arguments(years, "", False)
    fetch_response = fetcher.fetch_movies(args)
    assert isinstance(fetch_response, dict)
    assert fetch_response[1940][0] == 22


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_success_for_pages_more_than_100)
def test_fetch_success_for_pages_more_than_100(mock_post, mock_get, fetcher, years):
    """
    Test that successful fetching returns a dictionary and the correct number of movies for a given year
    when the number of pages is more than 100
    :param fetcher: fetcher instance
    """
    args = Arguments(years, "", False)
    fetch_response = fetcher.fetch_movies(args)
    assert isinstance(fetch_response, dict)
    assert fetch_response[1940][0] == 1002


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_success_with_search_term)
def test_fetch_success_with_search_term(mock_post, mock_get, fetcher, years):
    """
    Test that successful fetching returns a dictionary and the correct number of movies for a given year with search term
    :param mock_post:
    :param mock_get: mocks the response of the requests.get
    :param fetcher: fetcher instance
    :param years: years instance
    """
    args = Arguments(years, "test", False)
    fetch_response = fetcher.fetch_movies(args)
    assert isinstance(fetch_response, dict)
    assert fetch_response[1940][0] == 6


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_success_with_search_term)
def test_fetch_success_with_count_only(mock_post, mock_get, fetcher, years):
    """
    Test that successful fetching returns a dictionary and the correct number of movies for a given year with count only
    :param mock_post:
    :param mock_get: mocks the response of the requests.get
    :param fetcher: fetcher instance
    :param years: years instance
    """
    args = Arguments(years, "test", True)
    fetch_response = fetcher.fetch_movies(args)
    assert isinstance(fetch_response, dict)
    assert fetch_response[1940][0] == 6


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_success)
def test_process_years(mock_post, mock_get, fetcher):
    """
    Test that given same year multiple times as years argument returns a dictionary with the correct number of movies
    for a given year only once
    :param mock_post:
    :param mock_get: mocks the response of the requests.get
    :param fetcher: fetcher instance
    """
    args = Arguments([1940, 1940], "", False)
    fetch_response = fetcher.fetch_movies(args)
    assert type(fetch_response) is dict
    assert len(fetch_response) == 1


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_failure)
def test_fetch_failure(mock_post, mock_get, fetcher, years):
    """
    Test that unsuccessful fetching returns a dictionary with None for the specified year when year not found
    """
    args = Arguments(years, "", False)
    fetch_response = fetcher.fetch_movies(args)
    assert fetch_response[1940] is None
    assert fetch_response[1950] is None


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_auth_failure)
def test_fetch_auth_failure(mock_post, mock_get, fetcher, years):
    """
    Test that unsuccessful fetching returns a dictionary with None for the specified year when authentication fails
    """
    args = Arguments(years, "", False)
    fetch_response = fetcher.fetch_movies(args)
    assert fetch_response[1940] is None


@mock.patch("requests.post", side_effect=mocked_auth_success)
@mock.patch("requests.get", side_effect=mocked_fetch_exception_failure)
def test_fetch_exception_failure(mock_post, mock_get, fetcher, years):
    """
    Test that unsuccessful fetching returns a dictionary with None for the specified year when unexpected error occurs
    """
    args = Arguments(years, "", False)
    fetch_response = fetcher.fetch_movies(args)
    assert fetch_response[1940] is None
