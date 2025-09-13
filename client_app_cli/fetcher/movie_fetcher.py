from typing import List, Any
import requests
from client_app_cli.auth.authenticator import Authenticator
from client_app_cli.constants import constant

class MovieFetcher:
    """
    The movie fetcher is responsible for retrieving movie data from the API for the specified years.
    It uses an authenticator to authenticate the user by getting a bearer token and handles pagination for each year
    """
    def __init__(self, years: List[str], username: str, password: str) -> None:
        """
        Initialize the movie fetcher with the given username, password, and years

        :param years: List of years to fetch movie data for
        :param username: username to authenticate and obtain a bearer token
        :param password: password authenticate and obtain a bearer token
        """
        self.username = username
        self.password = password
        self.__process_years(years)

    def __process_years(self, years: List[str]):
        """
        convert the list of years into a set to get unique years
        """
        self.years = set(years)

    def fetch_movies(self) -> dict[Any, Any]:
        """
        Fetch movie data from the API for the specified years, handling authentication and pagination
        :return: A dictionary mapping each year to the count of movies fetched.
        """
        movies_counts = {}

        for year in self.years:
            page = 1
            total_movies = 0
            while True:
                # Authenticate every time for each request
                auth = Authenticator(self.username, self.password)
                bearer_token = auth.authenticate()
                headers = {'Authorization': f'Bearer {bearer_token}'}

                # Build the request URL
                url = constant.BASE_URL + constant.MOVIES_API.format(year=year, page=page)
                response = requests.get(url, headers=headers)

                # Check for HTTP error
                if response.status_code == 200:
                    movies = response.json()
                    total_movies += len(movies)

                    if len(movies) < 10:
                        break
                    page += 1
                else:
                    raise RuntimeError(response.json()['error'])
            movies_counts[year] = total_movies
        return movies_counts



