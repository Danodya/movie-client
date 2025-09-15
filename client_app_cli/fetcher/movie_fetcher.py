from typing import List, Any
import requests
from client_app_cli.auth.authenticator import Authenticator
from client_app_cli.exceptions.exceptions import AuthenticationException
from client_app_cli.constants import constant
from tqdm import tqdm


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

    def fetch_movies(self, years: List[int]) -> dict[Any, Any]:
        """
        Fetch movie data from the API for the specified years, handling authentication and pagination
        :return: A dictionary mapping each year to the count of movies fetched.
        """
        movies_counts: dict[Any, Any] = {}
        years = self.__process_years(years)

        # Initialize the progress bar
        with tqdm(
            total=len(years), desc="Fetching Movies by Year", unit="year"
        ) as pbar:
            for year in sorted(years):
                try:
                    pbar.set_postfix_str(f"Processing year={year}")
                    page = 1
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
                            movies_counts[year] = movies_counts.get(year, 0) + len(
                                movies
                            )

                            # stop when the last page is reached
                            if len(movies) < 10:
                                break
                            page += 1
                        else:
                            error_msg = response.json()["error"]
                            tqdm.write(f"{error_msg} for year {year}, page {page}")
                            movies_counts[year] = movies_counts.get(year, None)
                            break

                except AuthenticationException as e:
                    tqdm.write(f"{e} for year {year}")
                    movies_counts[year] = None

                except Exception as e:
                    tqdm.write(f"Unexpected error while fetching year {year}: {e}")
                    movies_counts[year] = None

                finally:
                    # Update the progress bar when a year finishes, regardless of success/failure
                    pbar.update(1)

        return movies_counts
