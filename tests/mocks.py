class MockSuccess:
    """
    Mocked response for successful operations
    """

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class MockFailure(MockSuccess):
    """
    Mocked response for failed operations
    """

    pass


def mocked_auth_success(*args, **kwargs):
    """
    Mocked response for successful authentication
    """

    return MockSuccess({"bearer": 1234, "timeout": 10}, 200)


def mocked_auth_failure(*args, **kwargs):
    """
    Mocked response for failed authentication
    """

    return MockFailure({"error": "invalid token"}, 401)


def mocked_fetch_success(*args, **kwargs):
    """
    Mocked response for successful fetch
    """
    return MockSuccess(["Title 1", "Title 2"], 200)


def mocked_fetch_with_more_than_10_movies(*args, **kwargs):
    """
    Mocked response for fetch movies with more than 10 movies to test pagination
    """
    return MockSuccess(
        [
            "Title 1",
            "Title 2",
            "Title 3",
            "Title 4",
            "Title 5",
            "Title 6",
            "Title 7",
            "Title 8",
            "Title 9",
            "Title 10",
            "Title 11",
            "Title 12",
        ],
        200,
    )


def mocked_fetch_failure(*args, **kwargs):
    """
    Mocked response for failed fetch for authentication failure
    """

    return MockFailure({"error": r"*.not found.*"}, 404)


def mocked_fetch_auth_failure(*args, **kwargs):
    """
    Mocked response for failed fetch for authentication failure
    """

    return MockFailure({"error": r"*.invalid.*"}, 401)


def mocked_fetch_exception_failure(*args, **kwargs):
    """
    Mocked response for failed fetch
    """

    return MockFailure(None, 401)
