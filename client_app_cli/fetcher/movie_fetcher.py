from typing import List


class MovieFetcher:
    def __init__(self, years: List[str], username: str, password: str) -> None:
        self.years = set(years)
        self.username = username
        self.password = password


