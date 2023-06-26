# Django
from django.shortcuts import render

# 3rd-party
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Project
from issue_tracking.models import Feedback
from issue_tracking.models import Report
from issue_tracking.serializers import FeedbackSerializer
from issue_tracking.serializers import ReportSerializer

# Create your views here.


class ReportList(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class FeedbackList(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
