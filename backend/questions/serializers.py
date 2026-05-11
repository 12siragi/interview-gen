"""
Serializers for the questions app.

The serializer is the FIRST line of defence.
It validates and cleans input BEFORE anything else runs.
If this fails, the AI service never gets called.
"""
from rest_framework import serializers

from .constants import MAX_JOB_TITLE_LENGTH


class QuestionRequestSerializer(serializers.Serializer):
    """
    Validates the incoming job title from the React frontend.

    Rules:
      - Must be a string
      - Minimum 2 characters — "a" is not a job title
        Note: single-character abbreviations are blocked here before
        ALLOWED_ABBREVIATIONS in validators.py is ever reached.
        Lower min_length to 1 if single-character roles need to be supported.
      - Maximum MAX_JOB_TITLE_LENGTH characters — imported from constants.py
        so the serializer and validator always agree on the same limit.
        Blocks oversized input and reduces prompt-injection surface area.
      - Whitespace trimmed — "  Engineer  " becomes "Engineer"
    """
    job_title = serializers.CharField(
        min_length=2,
        max_length=MAX_JOB_TITLE_LENGTH,
        trim_whitespace=True,
        error_messages={
            "blank":      "Job title cannot be blank.",
            "min_length": "Job title must be at least 2 characters.",
            "max_length": f"Job title must be {MAX_JOB_TITLE_LENGTH} characters or fewer.",
            "required":   "Job title is required.",
        },
    )