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
