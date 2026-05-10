"""
URL configuration for the questions app.

Single endpoint:
  POST /api/questions/generate/ → GenerateQuestionsView

Why POST not GET?
  GET requests are cached by browsers and proxies.
  A job title in the URL looks like:
    GET /api/questions/generate/?job_title=Engineer
  That gets cached, logged in server access logs, and
  stored in browser history — bad for dynamic AI responses.
  POST keeps the input in the request body — correct for this use case.
"""
from django.urls import path
from .views import GenerateQuestionsView

urlpatterns = [
    path("generate/", GenerateQuestionsView.as_view(), name="generate-questions"),
]
