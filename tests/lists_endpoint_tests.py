import unittest

import tests_config
from endpoint_test_case import EndpointTestCase

class TestListsEndpoint(EndpointTestCase):
    def test_get_lists(self):
        ''' Test basic all lists retrieval '''
        self.client.get_lists()

    def test_get_list(self):
        ''' Test getting of a specific list '''
        self.client.get_list(tests_config.ListsEndpointCfgValues.LIST_ID)

if __name__ == "__main__":
    unittest.main()
