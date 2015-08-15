import unittest
import wunderpy2

import tests_config
from endpoint_test_case import EndpointTestCase

class TestNotesEndpoint(EndpointTestCase):

    # Delete any leftover, hanging-around notes to return the state to what it was before we started
    @classmethod
    def setUpClass(cls):
        cls._leftover_notes = set()

    @classmethod
    def tearDownClass(cls):
        # TODO Delete leftover notes here
        pass

    def test_get_task_notes(self):
        self.client.get_task_notes(tests_config.NotesEndpointCfgValues.TASK_ID_WITH_NOTES)

    def test_get_list_notes(self):
        self.client.get_list_notes(tests_config.NotesEndpointCfgValues.LIST_ID)

    def test_get_note(self):
        task_notes = self.client.get_note(tests_config.NotesEndpointCfgValues.NOTE_ID)

    ''' 
    Disabled for now as there's a bug in Wunderlist API where you have to 
    call DELETE twice for the note to actually get deleted
    def test_crud_note(self):
        # create
        new_note = self.client.create_note(tests_config.NotesEndpointCfgValues.TASK_ID_WITHOUT_NOTES, "DELETE")
        new_note_id = new_note[wunderpy2.model.Note.id]
        new_note_revision = new_note[wunderpy2.model.Note.revision]

        # read
        retrieved_note = self.client.get_note(new_note_id)
        self.assertDictEqual(new_note, retrieved_note)

        # update
        new_content = "DELETEME"
        updated_note = self.client.update_note(new_note_id, new_note_revision, new_content)
        updated_content = updated_note[wunderpy2.model.Note.CONTENT]
        updated_revision = updated_note[wunderpy2.model.Note.revision]
        self.assertEqual(new_content, updated_content)

        # delete
        self.client.delete_note(new_note_id, updated_revision)
    '''

if __name__ == "__main__":
    unittest.main()
