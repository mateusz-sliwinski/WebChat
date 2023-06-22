from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from issue_tracking.serializers import ReportSerializer, FeedbackSerializer
from issue_tracking.models import Report, Feedback


# Create your views here.


class ReportList(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class FeedbackList(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
