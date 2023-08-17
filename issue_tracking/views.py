"""Views files."""
# 3rd-party
from rest_framework.generics import ListCreateAPIView

# Project
from issue_tracking.models import Feedback
from issue_tracking.models import Report
from issue_tracking.serializers import FeedbackSerializer
from issue_tracking.serializers import ReportSerializer


class ReportList(ListCreateAPIView):  # noqa: D101
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class FeedbackList(ListCreateAPIView):  # noqa: D101
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
