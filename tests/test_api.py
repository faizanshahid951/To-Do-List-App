import unittest
import json
import os
import shutil
import tempfile
from app import app, manager

class TestAppAPI(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage_file = os.path.join(self.test_dir, "test_api_tasks.json")
        manager.storage_path = self.storage_file
        manager._ensure_storage()
        self.client = app.test_client()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_and_fetch_task(self):
        # Create
        res = self.client.post("/api/tasks", json={
            "title": "Build Flask App",
            "description": "With clean UI",
            "priority": "High",
            "category": "Development"
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertEqual(data["title"], "Build Flask App")
        self.assertEqual(data["category"], "Development")
        task_id = data["id"]

        # Fetch list
        get_res = self.client.get("/api/tasks")
        self.assertEqual(get_res.status_code, 200)
        tasks = get_res.get_json()
        self.assertEqual(len(tasks), 1)

        # Toggle status
        toggle_res = self.client.patch(f"/api/tasks/{task_id}/toggle")
        self.assertEqual(toggle_res.status_code, 200)
        self.assertTrue(toggle_res.get_json()["completed"])

        # Stats
        stats_res = self.client.get("/api/stats")
        stats = stats_res.get_json()
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["completed"], 1)

        # Delete
        del_res = self.client.delete(f"/api/tasks/{task_id}")
        self.assertEqual(del_res.status_code, 200)

        # Verify empty
        get_res2 = self.client.get("/api/tasks")
        self.assertEqual(len(get_res2.get_json()), 0)

if __name__ == "__main__":
    unittest.main()
