"""Models files."""
# Django
from django.db import models


class Report(models.Model):  # noqa: D101
    description = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # noqa: D105
        return f'{self.reported_date}'


class Feedback(models.Model):  # noqa: D101
    description = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # noqa: D105
        return f'{self.feedback_date}'
