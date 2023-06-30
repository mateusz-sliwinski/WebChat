"""Serializers files."""
# 3rd-party
from rest_framework import serializers

# Project
from issue_tracking.models import Feedback
from issue_tracking.models import Report


class ReportSerializer(serializers.ModelSerializer):  # noqa: D101
    class Meta:  # noqa: D106
        model = Report
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):  # noqa: D101
    class Meta:  # noqa: D106
        model = Feedback
        fields = '__all__'
