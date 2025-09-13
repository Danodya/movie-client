def mocked_auth_success(*args, **kwargs):
    class MockSuccess:
        """
        Mocked response for successful authentication
        """
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockSuccess({"bearer": 1234, "timeout": 10}, 200)

def mocked_failure(*args, **kwargs):
    class MockFailure:
        """
        Mocked response for failed authentication
        """
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    return MockFailure({"error": "invalid token"}, 401)