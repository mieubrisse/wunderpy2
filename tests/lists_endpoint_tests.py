import unittest
import wunderpy2
import requests
import random
import string

import tests_config
from endpoint_test_case import EndpointTestCase

class TestListsEndpoint(EndpointTestCase):
    def setUp(self):
        ''' Does normal endpoint setup and also sets up tracking of any lists that were created during the course of testing '''
        super(TestListsEndpoint, self).setUp()
        # We set this up to track any lists that were created during the course of testing, so we can clean them up afterwards
        self._list_ids_to_cleanup = set()

    def tearDown(self):
        ''' Cleans up any lists created in the course of testing '''
        # TODO Obviously, this isn't ideal - it depends on the very functionality being tested - but the alternative is re-implementing list-specific delete logic here,
        #  which sucks worse.
        for list_id in self._list_ids_to_cleanup:
            try:
                list_obj = self.client.get_list(list_id)
                revision = list_obj[wunderpy2.model.List.revision]
                self.client.delete_list(list_id, revision)
            except ValueError:
                # There was an issue retrieving or deleting the list; it might be deleted already and we've done the best we can
                continue

    def _get_test_list(self):
        ''' Creates a new list with a random ID that gets cleaned up after the test is run '''
        random_title = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        # TODO It's not ideal that this depends on the 'create_list' function which is getting testsed, but the alternative is to re-implement list-creating logic,
        #  which is very fragile in case any of the Wunderlist stuff changes
        new_list = self.client.create_list(random_title)
        self._list_ids_to_cleanup.add(new_list[wunderpy2.model.List.id])
        return new_list

    def test_get_lists(self):
        ''' Test basic all lists retrieval '''
        self.client.get_lists()

    def test_get_list(self):
        ''' Test getting of a specific list '''
        new_list = self._get_test_list()
        new_list_id = new_list[wunderpy2.model.List.id]
        retrieved_list = self.client.get_list(new_list_id)
        self.assertDictEqual(new_list, retrieved_list)

    def test_create_list(self):
        ''' Test list creation '''
        new_list = self.client.create_list("PLZ_DELETE")
        self._list_ids_to_cleanup.add(new_list[wunderpy2.model.List.id])

    def test_update_list(self):
        ''' Test updating list '''
        new_list = self._get_test_list()
        new_list_id = new_list[wunderpy2.model.List.id]
        new_list_revision = new_list[wunderpy2.model.List.revision]
        new_list_public = new_list[wunderpy2.model.List.public]

        updated_title = "DELETEME!"
        updated_public = not new_list_public
        updated_list = self.client.update_list(new_list_id, new_list_revision, title=updated_title, public=updated_public)
        self.assertEqual(updated_public, updated_list[wunderpy2.model.List.public])
        self.assertEqual(updated_title, updated_list[wunderpy2.model.List.title])

    def test_delete_list(self):
        ''' Test list deletion '''
        new_list = self._get_test_list()
        new_list_id = new_list[wunderpy2.model.List.id]
        new_list_revision = new_list[wunderpy2.model.List.revision]
        self.client.delete_list(new_list_id, new_list_revision)
        self.assertRaises(ValueError, self.client.get_list, new_list_id)

if __name__ == "__main__":
    unittest.main()
