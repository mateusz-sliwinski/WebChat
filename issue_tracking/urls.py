"""Urls.py files."""

# Django
from django.urls import path

# Project
from issue_tracking.views import FeedbackList
from issue_tracking.views import ReportList

urlpatterns = [
    path('report/', ReportList.as_view()),
    path('feedback/', FeedbackList.as_view()),
]
