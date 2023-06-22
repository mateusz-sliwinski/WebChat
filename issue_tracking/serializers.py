# 3rd-party
from rest_framework import serializers

# Project
from issue_tracking.models import Feedback
from issue_tracking.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
