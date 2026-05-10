"""
Views for the questions app.

Design principle: keep views THIN.
  - Validation  → serializer handles it
  - AI logic    → ai_service handles it
  - The view only coordinates between them

This makes each layer independently testable.
"""
import logging

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .ai_service import generate_interview_questions
from .serializers import QuestionRequestSerializer

logger = logging.getLogger(__name__)


class GenerateQuestionsView(APIView):
    """
    POST /api/questions/generate/

    Accepts:  { "job_title": "Customer Success Manager" }
    Returns:  { "questions": ["Q1?", "Q2?", "Q3?"] }

    Error responses:
      400 — invalid input (blank, too short, too long)
      500 — AI provider error or parse failure
    """

    def post(self, request):
        # ── Step 1: Validate input ────────────────────────────────────────────
        serializer = QuestionRequestSerializer(data=request.data)

        if not serializer.is_valid():
            # 400 errors are descriptive — help the user fix their input
            logger.warning(
                "Invalid request: %s", serializer.errors
            )
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job_title = serializer.validated_data["job_title"]
        client_ip = request.META.get("HTTP_X_FORWARDED_FOR", 
                    request.META.get("REMOTE_ADDR", "unknown"))
        logger.info("generate_request ip=%s title_length=%d", 
                   client_ip, len(job_title))

        # ── Step 2: Generate questions ────────────────────────────────────────
        try:
            questions = generate_interview_questions(job_title)

            logger.info(
                "Successfully generated questions for '%s'", job_title
            )

            return Response(
                {"questions": questions},
                status=status.HTTP_200_OK,
            )

        except ValueError as exc:
            # Configuration error or parse failure
            # Log full detail — return safe message to client
            logger.error(
                "ValueError generating questions for '%s': %s",
                job_title, exc
            )
            return Response(
                {"error": "Failed to generate questions. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except requests.HTTPError as exc:
            # AI provider returned a non-200 status
            # Log full detail — return safe message to client
            logger.error(
                "AI provider HTTP error for '%s': %s",
                job_title, exc
            )
            return Response(
                {"error": "AI provider error. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as exc:
            # Catch-all — unexpected failures
            # Never expose internal error details to the client
            logger.exception(
                "Unexpected error generating questions for '%s'", job_title
            )
            return Response(
                {"error": "An unexpected error occurred. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
