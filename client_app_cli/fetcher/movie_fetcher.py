import concurrent.futures
from typing import List, Any
import requests
from requests import Response

from client_app_cli.arguments.arguments import Arguments
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

    @staticmethod
    def __process_years(years: List[int]):
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

    def fetch_movies(self, args: Arguments) -> dict[Any, Any]:
        """
        Fetch movie data from the API for the specified years, handling authentication and pagination
        :return: A dictionary mapping each year to the count of movies fetched.
        """
        movies_counts: dict[Any, Any] = {}
        years = self.__process_years(args.years)
        search_term = args.search_term

        for year in sorted(years):
            filtered_movies: Any = []
            try:
                page = self.find_lowest_failing_page_for_year(year)

                if not search_term:
                    response = self.fetch(page - 1, year)
                    movies = response.json()
                    movies_counts[year] = [10 * (page - 2) + len(movies), None]
                else:
                    search_term_lower = search_term.lower()
                    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                        futures = {
                            executor.submit(
                                self.fetch_and_filter, p, year, search_term_lower
                            )
                            for p in range(1, page)
                        }
                        for future in concurrent.futures.as_completed(futures):
                            try:
                                result = future.result()
                                filtered_movies.extend(result)
                            except Exception as e:
                                print(f"Error occurred while fetching: {e}")

                    movies_counts[year] = [len(filtered_movies), filtered_movies]

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
        :param page: number to fetch
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

    def fetch_and_filter(self, page: int, year: int, search_term: str) -> List[str]:
        """
        Fetch movies for given year and page and filter them based on the search term
        :param page: page number to fetch
        :param year: year to fetch movies
        :param search_term: term to filter movies(case-insensitive)
        :return: List of filtered movies
        """
        response = self.fetch(page, year)
        movies = response.json()
        filtered_movies = [
            movie for movie in movies if search_term in movie.lower()
        ]
        return filtered_movies
