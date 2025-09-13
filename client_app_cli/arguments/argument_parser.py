import argparse


class ArgumentParser:
    """
    Handles command-line argument parsing for the Movie Fetcher CLI.
    Provides methods to define and parse arguments for fetching movies by given years
    """

    def __init__(self):
        """
        Initialize the argument parser and set up the argument definitions
        """
        self.parser = argparse.ArgumentParser(
            prog="Movie-Client", description="Movie Client - Fetch movies from the database")

    def add_arguments(self):
        """
        Defines the command-line arguments for the parser.
        Adds 'years' arguments to the parser.
        """
        self.parser.add_argument(
            "-y", "--year", required=True, nargs="+", type=int,
            help="The years to fetch movies for (e.g., y 1940 1950)")

    def parse(self) -> argparse.Namespace:
        """
        Parse and return the CLI arguments.
        """
        return self.parser.parse_args()