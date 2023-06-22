from django.db import models


# Create your models here.

class Report(models.Model):
    description = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # noqa: D105
        return f'{self.reported_date}'


class Feedback(models.Model):
    description = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # noqa: D105
        return f'{self.feedback_date}'
