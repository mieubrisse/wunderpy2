import unittest
import wunderpy2

import tests_config

class EndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = wunderpy2.WunderClient(tests_config.ACCESS_TOKEN, tests_config.CLIENT_ID)
