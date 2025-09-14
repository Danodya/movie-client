from typing import List, Any, Optional
import requests
from client_app_cli.auth.authenticator import Authenticator
from client_app_cli.exceptions.exceptions import MovieFetchException
from client_app_cli.constants import constant
from tqdm import tqdm


class MovieFetcher:
    """
    The movie fetcher is responsible for retrieving movie data from the API for the specified years.
    It uses an authenticator to authenticate the user by getting a bearer token and handles pagination for each year
    """

    def __init__(self, years: List[str], authenticator: Authenticator) -> None:
        """
        Initialize the movie fetcher with the given username, password, and years

        :param years: List of years to fetch movie data for
        :param authenticator: Instance to obtain bearer token for API requests
        """
        self.authenticator = authenticator
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
        movies_counts: dict[Any, Any] = {}

        # Initialize the progress bar
        with tqdm(
            total=len(self.years), desc="Fetching Movies by Year", unit="year"
        ) as pbar:
            for year in self.years:
                try:
                    pbar.set_postfix({"year": year})
                    page = 1
                    total_movies = 0
                    while True:
                        # Authenticate every time for each request
                        bearer_token = self.authenticator.authenticate()

                        # Build the request URL
                        url = self.authenticator.base_url + constant.MOVIES_API.format(
                            year=year, page=page
                        )
                        headers = {"Authorization": f"Bearer {bearer_token}"}
                        response = requests.get(url, headers=headers)

                        # Check for HTTP error
                        if response.status_code == 200:
                            movies = response.json()
                            total_movies += len(movies)

                            # stop when the last page is reached
                            if len(movies) < 10:
                                break
                            page += 1
                        else:
                            raise MovieFetchException(response.json()["error"])

                    movies_counts[year] = total_movies

                except Exception as e:
                    error_msg = f"Error fetching {year}: {e}"
                    print(f"{error_msg}")
                    movies_counts[year] = None

                finally:
                    # Update the progress bar when a year finishes, regardless of success/failure
                    pbar.update(1)

        return movies_counts
