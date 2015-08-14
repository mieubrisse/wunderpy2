import unittest

import tests_config
from wunderclient_test_case import WunderclientTestCase


class TestTasksEndpoint(WunderclientTestCase):
    def test_get_task_notes(self):
        self.client.get_task_notes(tests_config.TASK_ID_WITH_NOTES)

    def test_get_list_notes(self):
        self.client.get_list_notes(tests_config.INBOX_ID)

'''
    def test_task_creation(self):
        # client.get_lists()
        test_list_id = self.config[wp_t_config.ConfigKeys.INBOX_ID]
        response = self.client.create_task(test_list_id, "Test create task")
        self.assertEqual(response.status_code, 201)

# TODO Try creating a task with a non-existent list
# TODO Try creating a task with a task with a string for list ID
# TODO Try creating a task with too long of a title

print "Updating task..."
updated_task = client.update_task(created_task[wunderpy2.Task.id], created_task[wunderpy2.Task.revision], title="New title")

# TODO Try updating a task with known out-of-date revision
# TODO Try updating a non-existent task ID
# TODO Try updating a task with too long a title
# TODO Try removing some properties from a task

print "Deleting task..."
client.delete_task(updated_task[wunderpy2.Task.id], updated_task[wunderpy2.Task.revision])
print "Deleting already-deleted task..."
# This should fail with a 404
try:
    client.delete_task(updated_task[wunderpy2.Task.id], updated_task[wunderpy2.Task.revision])
except ValueError:
    print "Caught ValueError as expected"
    pass

# TODO Try deleting a task with out-of-date revision
'''

if __name__ == "__main__":
    unittest.main()
