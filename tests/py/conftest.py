"""
Shared test fixtures and base classes for pytest.
"""
import json
import os
import unittest


class EndpointBaseTest(unittest.TestCase):
    """
    Base class for testing endpoints.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointBaseTest, self).__init__(*args, **kwargs)

    def get_file_path(self, filename):
        return os.path.join(os.path.dirname(__file__), "data", filename)

    def get_content(self, filename):
        with open(self.get_file_path(filename)) as f:
            return f.read()

    def get_content_in_json(self, filename):
        with open(self.get_file_path(filename)) as f:
            return json.loads(f.read())

