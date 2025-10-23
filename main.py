import os

from client_app_cli.arguments.argument_parser import ArgumentParser
from client_app_cli.arguments.arguments import Arguments
from client_app_cli.auth.authenticator import Authenticator
from client_app_cli.constants.constant import (
    DEFAULT_USERNAME,
    DEFAULT_PASSWORD,
    BASE_URL,
)
from client_app_cli.fetcher.movie_fetcher import MovieFetcher
from client_app_cli.pretty_print.pretty_print import PrettyPrinter

if __name__ == "__main__":
    print("Starting movie-client...")

    argument_parser = ArgumentParser()
    args = Arguments(
        argument_parser.parse().years,
        argument_parser.parse().search,
        argument_parser.parse().count_only,
    )

    username = os.environ.get("MOVIE_API_USERNAME", DEFAULT_USERNAME)
    password = os.environ.get("MOVIE_API_PASSWORD", DEFAULT_PASSWORD)
    base_url = os.environ.get("MOVIE_API_BASE_URL", BASE_URL)

    auth = Authenticator(username, password, base_url)
    fetcher = MovieFetcher(auth)

    response = fetcher.fetch_movies(args)
    PrettyPrinter.pretty_print(response, args)
