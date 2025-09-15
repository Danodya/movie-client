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


def mocked_fetch_failure(*args, **kwargs):
    """
    Mocked response for failed fetch
    """

    return MockFailure({"error": r"*.not found.*"}, 404)
