"""Urls.py files."""

# Django
from django.urls import path


from issue_tracking.views import ReportList, FeedbackList

urlpatterns = [
    path('report/', ReportList.as_view()),
    path('feedback/', FeedbackList.as_view()),
]
