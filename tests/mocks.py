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


def mocked_fetch_success(url, **kwargs):
    """
    Mocked response for successful fetch
    """
    page = int(url.rstrip("/").split("/")[-1])
    if page == 1:
        return MockSuccess([{}] * 10, 200)  # 10 movies
    if page == 2:
        return MockSuccess([{}] * 10, 200)  # 10 movies
    if page == 3:
        return MockSuccess([{}] * 2, 200)
    else:
        return MockFailure({"error": r"*.not found.*"}, 404)


def mocked_fetch_success_for_pages_more_than_100(url, **kwargs):
    """
    Mocked response for successful fetch for pages more than 100
    """
    page = int(url.rstrip("/").split("/")[-1])
    if page == 100:
        return MockSuccess([{}] * 10, 200)  # 10 movies
    if page == 101:
        return MockSuccess([{}] * 2, 200)
    else:
        return MockFailure({"error": r"*.not found.*"}, 404)


def mocked_fetch_success_with_search_term(url, **kwargs):
    """
    Mocked response for successful fetch with search term
    """
    page = int(url.rstrip("/").split("/")[-1])
    if page == 1:
        return MockSuccess(
            [
                "testing",
                "test",
                "star",
                "movie1",
                "movie2",
                "movie3",
                "movie4",
                "movie5",
                "movie6",
                "movie7",
            ],
            200,
        )  # 10 movies
    if page == 2:
        return MockSuccess(
            [
                "testing",
                "test",
                "star",
                "movie1",
                "movie2",
                "movie3",
                "movie4",
                "movie5",
                "movie6",
                "movie7",
            ],
            200,
        )  # 10 movies
    if page == 3:
        return MockSuccess(["testing", "test", "star"], 200)
    else:
        return MockFailure({"error": r"*.not found.*"}, 404)


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
