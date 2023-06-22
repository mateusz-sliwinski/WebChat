from django.contrib import admin

# Register your models here.
from issue_tracking.models import Report, Feedback


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):  # noqa D101
    readonly_fields = ('reported_date',)
    list_display = [
        'description',
        'reported_date',
    ]
    list_filter = [
        'reported_date',
    ]


@admin.register(Feedback)
class ReportAdmin(admin.ModelAdmin):  # noqa D101
    readonly_fields = ('feedback_date',)
    list_display = [
        'description',
        'feedback_date',
    ]
    list_filter = [
        'feedback_date',
    ]
