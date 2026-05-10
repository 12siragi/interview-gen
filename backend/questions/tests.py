"""
Tests for the questions app.

Testing philosophy: test behaviour not implementation.
We test what the endpoint DOES, not how it does it.
"""
from unittest.mock import patch
from django.test import TestCase, Client
import json


class GenerateQuestionsViewTest(TestCase):
    """Tests for POST /api/questions/generate/"""

    def setUp(self):
        self.client = Client()
        self.url = "/api/questions/generate/"
        self.valid_payload = {"job_title": "Customer Success Manager"}

    def test_valid_request_returns_200(self):
        """Valid job title should return 200 with 3 questions."""
        mock_questions = [
            "Tell me about a time you retained a customer?",
            "How do you measure customer health?",
            "Describe your onboarding process."
        ]
        with patch("questions.views.generate_interview_questions") as mock_ai:
            mock_ai.return_value = mock_questions
            response = self.client.post(
                self.url,
                data=json.dumps(self.valid_payload),
                content_type="application/json"
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("questions", data)
        self.assertEqual(len(data["questions"]), 3)

    def test_empty_job_title_returns_400(self):
        """Empty job title should return 400."""
        response = self.client.post(
            self.url,
            data=json.dumps({"job_title": ""}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_job_title_returns_400(self):
        """Missing job_title field should return 400."""
        response = self.client.post(
            self.url,
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_job_title_too_short_returns_400(self):
        """Single character job title should return 400."""
        response = self.client.post(
            self.url,
            data=json.dumps({"job_title": "a"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_job_title_too_long_returns_400(self):
        """Job title over 120 chars should return 400."""
        response = self.client.post(
            self.url,
            data=json.dumps({"job_title": "x" * 121}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_ai_failure_returns_500(self):
        """AI service failure should return 500 with safe message."""
        with patch("questions.views.generate_interview_questions") as mock_ai:
            mock_ai.side_effect = ValueError("API key missing")
            response = self.client.post(
                self.url,
                data=json.dumps(self.valid_payload),
                content_type="application/json"
            )

        self.assertEqual(response.status_code, 500)
        data = response.json()
        # Safe message — no internal details exposed
        self.assertNotIn("API key", data.get("error", ""))

    def test_get_request_not_allowed(self):
        """GET should not be allowed — only POST."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
