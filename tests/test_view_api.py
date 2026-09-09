import unittest

from fastapi.testclient import TestClient

from main import app


class ViewApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_view_accepts_case_insensitive_patient_id(self):
        response = self.client.get("/view/p001")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Rahul Sharma")

    def test_view_reports_missing_id_with_available_options(self):
        response = self.client.get("/view/PAT1002")
        self.assertEqual(response.status_code, 404)
        self.assertIn("P001", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
