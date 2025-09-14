import os

from client_app_cli.arguments.argument_parser import ArgumentParser
from client_app_cli.auth.authenticator import Authenticator
from client_app_cli.constants.constant import (
    DEFAULT_USERNAME,
    DEFAULT_PASSWORD,
    BASE_URL,
)
from client_app_cli.fetcher.movie_fetcher import MovieFetcher

if __name__ == "__main__":
    print("Starting the application...")

    argument_parser = ArgumentParser()
    years = argument_parser.parse().years

    username = os.environ.get("USERNAME", DEFAULT_USERNAME)
    password = os.environ.get("PASSWORD", DEFAULT_PASSWORD)
    base_url = os.environ.get("BASE_URL", BASE_URL)

    auth = Authenticator(username, password, base_url)
    fetcher = MovieFetcher(years, auth)

    response = fetcher.fetch_movies()

    if response:
        for year, count in response.items():
            if count is None:
                print()

        pretty_response = "\n".join(
            [
                (
                    f"Failed to fetch movies for year {key}."
                    if response[key] is None
                    else f"Year {key} has {response[key]} movies."
                )
                for key in response
            ]
        )
        print(pretty_response)
    else:
        print("No response received.")
