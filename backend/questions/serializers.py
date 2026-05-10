"""
Serializers for the questions app.

The serializer is the FIRST line of defence.
It validates and cleans input BEFORE anything else runs.
If this fails, the AI service never gets called.
"""
from rest_framework import serializers


class QuestionRequestSerializer(serializers.Serializer):
    """
    Validates the incoming job title from the React frontend.

    Rules:
      - Must be a string
      - Minimum 2 characters — "a" is not a job title
      - Maximum 120 characters — blocks oversized input and prompt injection
      - Whitespace trimmed — "  Engineer  " becomes "Engineer"
    """
    job_title = serializers.CharField(
        min_length=2,
        max_length=120,
        trim_whitespace=True,
        error_messages={
            "blank":      "Job title cannot be blank.",
            "min_length": "Job title must be at least 2 characters.",
            "max_length": "Job title must be 120 characters or fewer.",
            "required":   "Job title is required.",
        },
    )
