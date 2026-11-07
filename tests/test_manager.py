import unittest
import os
import shutil
import tempfile
from core.manager import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage_file = os.path.join(self.test_dir, "test_tasks.json")
        self.manager = TaskManager(storage_path=self.storage_file)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_and_get_task(self):
        task = self.manager.add_task(title="Buy Groceries", description="Milk, Eggs", priority="High", category="Personal")
        self.assertEqual(task.title, "Buy Groceries")
        self.assertEqual(task.priority, "High")
        self.assertFalse(task.completed)

        tasks = self.manager.get_all()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, task.id)

    def test_toggle_task(self):
        task = self.manager.add_task(title="Read Book")
        toggled = self.manager.toggle_task(task.id)
        self.assertTrue(toggled.completed)

        toggled_again = self.manager.toggle_task(task.id)
        self.assertFalse(toggled_again.completed)

    def test_update_task(self):
        task = self.manager.add_task(title="Old Title")
        updated = self.manager.update_task(task.id, {"title": "New Title", "priority": "High"})
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.priority, "High")

    def test_delete_task(self):
        task = self.manager.add_task(title="To be deleted")
        deleted = self.manager.delete_task(task.id)
        self.assertTrue(deleted)
        self.assertEqual(len(self.manager.get_all()), 0)

    def test_filters_and_search(self):
        self.manager.add_task(title="Python homework", category="Study", priority="High")
        t2 = self.manager.add_task(title="Gym workout", category="Health", priority="Low")
        self.manager.toggle_task(t2.id)

        self.assertEqual(len(self.manager.get_all(status="active")), 1)
        self.assertEqual(len(self.manager.get_all(status="completed")), 1)
        self.assertEqual(len(self.manager.get_all(search="homework")), 1)
        self.assertEqual(len(self.manager.get_all(priority="high")), 1)

if __name__ == "__main__":
    unittest.main()
