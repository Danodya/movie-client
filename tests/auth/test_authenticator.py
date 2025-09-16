from unittest import mock

import pytest

from client_app_cli.auth.authenticator import Authenticator
from client_app_cli.constants.constant import (
    DEFAULT_USERNAME,
    DEFAULT_PASSWORD,
    BASE_URL,
)
from client_app_cli.exceptions.exceptions import AuthenticationException
from tests.mocks import mocked_auth_success, mocked_auth_failure


def test_validate_success():
    """
    Test that valid username and password do not raise exceptions
    """
    Authenticator(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)


def test_validate_invalid_username():
    """
    Test that invalid username raises AuthenticationException
    """
    with pytest.raises(
        AuthenticationException, match=r".*username must be a non-empty string.*"
    ):
        Authenticator("", DEFAULT_PASSWORD, BASE_URL)


def test_validate_invalid_password():
    """
    Test that invalid password raises AuthenticationException
    """
    with pytest.raises(
        AuthenticationException, match=r".*password must be a non-empty string.*"
    ):
        Authenticator(DEFAULT_USERNAME, "", BASE_URL)


def test_validate_invalid_url():
    """
    Test that an invalid url raises AuthenticationException
    """
    with pytest.raises(
        AuthenticationException, match=r".*URL must be valid and non-empty string.*"
    ):
        Authenticator(DEFAULT_USERNAME, DEFAULT_PASSWORD, "#invalid-url")


@mock.patch("requests.post", side_effect=mocked_auth_success)
def test_authenticate_success(mock_post):
    """
    Test that successful authentication returns correct bearer token
    :param mock_post: mocks the response of the requests.post
    :return: bearer token
    """
    auth_response = Authenticator(
        DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL
    ).authenticate()
    assert auth_response == 1234
    mock_post.assert_called_once()


@mock.patch("requests.post", side_effect=mocked_auth_failure)
def test_authenticate_failure(mock_post):
    """
    Test that unsuccessful authentication raises AuthenticationException
    :param mock_post: mocks the response of the requests.post
    """
    with pytest.raises(AuthenticationException, match=r".*invalid token*"):
        Authenticator(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL).authenticate()
