from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from auth_app.models import DashboardWidget, UserActivity, Report
import json
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the database with sample data for demonstration'

    def handle(self, *args, **options):
        # Create sample widgets
        widgets_data = [
            {
                'title': 'Total Users',
                'widget_type': 'stat',
                'description': 'Current number of registered users',
                'data': {'value': '1,234'}
            },
            {
                'title': 'Monthly Reports',
                'widget_type': 'chart',
                'description': 'Reports generated this month',
                'data': {'chart_type': 'line', 'value': '89'}
            },
            {
                'title': 'Recent Activities',
                'widget_type': 'activity',
                'description': 'Latest user activities',
                'data': {}
            },
            {
                'title': 'System Status',
                'widget_type': 'news',
                'description': 'Current system status and updates',
                'data': {'content': '✅ All systems operational\n📊 Database performance: Excellent\n🔒 Security: Up to date'}
            },
            {
                'title': 'User Statistics',
                'widget_type': 'table',
                'description': 'Detailed user statistics',
                'data': {'rows': 15, 'columns': 4}
            }
        ]

        for widget_data in widgets_data:
            widget, created = DashboardWidget.objects.get_or_create(
                title=widget_data['title'],
                defaults=widget_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created widget: {widget.title}'))

        # Create sample activities
        if User.objects.exists():
            user = User.objects.first()
            activities_data = [
                {'activity_type': 'login', 'description': 'User logged in from web browser'},
                {'activity_type': 'report_generated', 'description': 'Generated monthly analytics report'},
                {'activity_type': 'profile_updated', 'description': 'Updated profile information'},
                {'activity_type': 'dashboard_viewed', 'description': 'Accessed main dashboard'},
                {'activity_type': 'widget_created', 'description': 'Created new dashboard widget'},
            ]

            for i, activity_data in enumerate(activities_data):
                # Create activities with different timestamps
                timestamp = datetime.now() - timedelta(hours=i*2)
                UserActivity.objects.create(
                    user=user,
                    activity_type=activity_data['activity_type'],
                    description=activity_data['description'],
                    timestamp=timestamp
                )
                self.stdout.write(self.style.SUCCESS(f'Created activity: {activity_data["activity_type"]}'))

        # Create sample reports
        if User.objects.exists():
            user = User.objects.first()
            reports_data = [
                {
                    'title': 'Monthly User Report',
                    'report_type': 'monthly',
                    'data': {
                        'summary': 'This month saw a 25% increase in user registrations compared to last month.',
                        'total_users': 1234,
                        'new_users': 156,
                        'active_users': 892
                    }
                },
                {
                    'title': 'Weekly Analytics',
                    'report_type': 'weekly',
                    'data': {
                        'summary': 'Dashboard usage increased by 15% this week.',
                        'page_views': 5678,
                        'unique_visitors': 1234,
                        'avg_session_time': '4m 32s'
                    }
                }
            ]

            for report_data in reports_data:
                report, created = Report.objects.get_or_create(
                    title=report_data['title'],
                    defaults={
                        **report_data,
                        'generated_by': user,
                        'is_public': True
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created report: {report.title}'))

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))
