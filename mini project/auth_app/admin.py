from django.contrib import admin
from .models import (
    UserProfile,
    DashboardWidget,
    UserActivity,
    Report,
    Complaint,
)

# User Profile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "created_at")
    search_fields = ("user__username", "phone_number")


# Dashboard Widgets
@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ("title", "widget_type", "is_active", "created_at")
    list_filter = ("widget_type", "is_active")
    search_fields = ("title",)


# User Activity
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "activity_type", "timestamp", "ip_address")
    list_filter = ("activity_type", "timestamp")
    search_fields = ("user__username", "activity_type", "description", "ip_address")


# Reports (JSON-backed)
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "report_type", "generated_by", "is_public", "generated_at")
    list_filter = ("report_type", "is_public", "generated_at")
    search_fields = ("title", "generated_by__username")


# Complaints (community issues)
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "location", "likes", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "location", "user__username")
