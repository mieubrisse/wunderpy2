import unittest
import wunderpy2

import tests_config

class EndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.api = wunderpy2.WunderApi()
        self.client = self.api.get_client(tests_config.ACCESS_TOKEN, tests_config.CLIENT_ID)
