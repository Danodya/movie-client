from typing import List, Any
import requests
from requests import Response

from client_app_cli.auth.authenticator import Authenticator
from client_app_cli.exceptions.exceptions import (
    AuthenticationException,
    MovieFetcherException,
)
from client_app_cli.constants import constant


class MovieFetcher:
    """
    The movie fetcher is responsible for retrieving movie data from the API for the specified years.
    It uses an authenticator to authenticate the user by getting a bearer token and handles pagination for each year
    """

    def __init__(self, authenticator: Authenticator) -> None:
        """
        Initialize the movie fetcher with Authenticator object.
        :param authenticator: Instance to obtain bearer token for API requests
        """
        self.authenticator = authenticator

    def __process_years(self, years: List[int]):
        """
        convert the list of years into a set to get unique years
        """
        return set(years)

    def find_lowest_failing_page_for_year(self, year: int) -> int:
        lower = 1
        upper = 100
        page = upper

        while True:
            # do the exponential growth to get the failing page
            response = self.fetch(page, year)
            if response.status_code == 200:
                lower = page + 1
                upper = 2 * page
                page = upper
            else:
                break

        # Do binary search to find the lowest failing page
        while lower <= upper:
            mid = lower + (upper - lower) // 2
            page = mid
            response = self.fetch(page, year)
            # Check for HTTP error
            if response.status_code == 200:
                lower = page + 1
            else:
                upper = page - 1
        if page == 1 and lower == 1:
            raise MovieFetcherException(response.json()["error"])

        return page


    def fetch_movies(self, years: List[int]) -> dict[Any, Any]:
        """
        Fetch movie data from the API for the specified years, handling authentication and pagination
        :return: A dictionary mapping each year to the count of movies fetched.
        """
        movies_counts: dict[Any, Any] = {}
        years = self.__process_years(years)

        for year in sorted(years):
            try:
                page = self.find_lowest_failing_page_for_year(year)
                response = self.fetch(page - 1, year)
                movies = response.json()
                movies_counts[year] = 10 * (page - 2) + len(movies)

            except (AuthenticationException, MovieFetcherException) as e:
                print(f"{e} for year {year}")
                movies_counts[year] = None

            except Exception as e:
                print(f"Unexpected error while fetching year {year}: {e}")
                movies_counts[year] = None
        return movies_counts

    def fetch(self, page: int, year: int) -> Response:
        """
        Fetch movies for given year and page
        :param page: page number to fetch
        :param year: year to fetch movies
        :return: Response object for the fetched movies
        """
        # Authenticate every time for each request
        bearer_token = self.authenticator.authenticate()

        # Build the request URL
        url = self.authenticator.base_url + constant.MOVIES_API.format(
            year=year, page=page
        )
        headers = {"Authorization": f"Bearer {bearer_token}"}
        response = requests.get(url, headers=headers)
        return response
