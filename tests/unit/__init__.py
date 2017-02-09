import os
import json
import unittest


class EndpointBaseUnitTest(unittest.TestCase):
    """
    Base class for testing endpoints.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointBaseUnitTest, self).__init__(*args, **kwargs)
        self.host = 'platform.exabyte.io'
        self.port = 4000

    def get_file_path(self, filename):
        return os.path.join(os.path.dirname(__file__), '..', 'data', filename)

    def get_content_in_json(self, filename):
        with open(self.get_file_path(filename)) as f:
            return json.loads(f.read())
