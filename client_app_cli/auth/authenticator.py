import requests
from client_app_cli.constants import constant
from client_app_cli.exceptions.exceptions import AuthenticationException
from urllib.parse import urlparse


class Authenticator:
    """
    Authenticator class that handles authentication
    """

    def __init__(self, username: str, password: str, base_url: str):
        """
        Initializes the Authenticator with user credentials

        :param username: Username for authentication
        :param password: Password for authentication
        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.__validate()

    def __validate(self):
        """
        Validates the username, password, and base_url.
        Raises AuthenticationException if any validation fails.
        """
        if not self.username or not isinstance(self.username, str):
            raise AuthenticationException("username must be a non-empty string")
        if not self.password or not isinstance(self.password, str):
            raise AuthenticationException("password must be a non-empty string")
        if not self.base_url or not self.__is_valid_url(self.base_url):
            raise AuthenticationException("URL must be valid and non-empty string")

    def __is_valid_url(self, url: str) -> bool:
        """
        Validates if the provided string is a valid URL.
        :param url: The URL string to validate.
        :return: True if the URL is valid, False otherwise.
        """
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])

    def authenticate(self) -> str:
        """
        Authenticates the user using the username and password provided at instantiation.
        :return: bearer token
        """
        url = self.base_url + constant.AUTH_API
        payload = {"username": self.username, "password": self.password}
        response = requests.post(
            url, json=payload, headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            bearer_token = response.json()["bearer"]
        else:
            raise AuthenticationException(response.json()["error"])
        return bearer_token
