from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, DashboardWidget, UserActivity, Report, Complaint
import json

def home(request):
    # Get active dashboard widgets
    widgets = DashboardWidget.objects.filter(is_active=True)

    # Get recent activities
    recent_activities = UserActivity.objects.all()[:10]

    # Get recent reports
    recent_reports = Report.objects.filter(is_public=True).order_by('-generated_at')[:5]
    
    # Get all complaints ordered by creation date (newest first)
    complaints = Complaint.objects.all().order_by('-created_at')

    # Log user visit if authenticated
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            activity_type='page_visit',
            description=f'Visited dashboard/home page',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

    context = {
        'widgets': widgets,
        'recent_activities': recent_activities,
        'recent_reports': recent_reports,
        'complaints': complaints,
    }

    return render(request, 'index.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)

                # Log login activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    description='User logged in successfully',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )

                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('main_app')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please check your login credentials.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create user profile
            UserProfile.objects.create(user=user)

            # Log registration activity
            UserActivity.objects.create(
                user=user,
                activity_type='registration',
                description='New user account created',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        # Log logout activity
        UserActivity.objects.create(
            user=request.user,
            activity_type='logout',
            description='User logged out',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    # Get user activities
    user_activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')[:20]

    # Get user reports
    user_reports = Report.objects.filter(generated_by=request.user).order_by('-generated_at')[:10]

    context = {
        'user': request.user,
        'user_activities': user_activities,
        'user_reports': user_reports,
    }

    return render(request, 'profile.html', context)

@login_required
def dashboard_view(request):
    """View for managing dashboard widgets"""
    widgets = DashboardWidget.objects.all()

    if request.method == 'POST':
        if 'add_widget' in request.POST:
            widget = DashboardWidget.objects.create(
                title=request.POST.get('title'),
                widget_type=request.POST.get('widget_type'),
                description=request.POST.get('description', ''),
                data=request.POST.get('data', '{}')
            )
            messages.success(request, f'Widget "{widget.title}" created successfully!')

        elif 'toggle_widget' in request.POST:
            widget_id = request.POST.get('widget_id')
            widget = DashboardWidget.objects.get(id=widget_id)
            widget.is_active = not widget.is_active
            widget.save()
            status = "activated" if widget.is_active else "deactivated"
            messages.success(request, f'Widget "{widget.title}" {status}!')

        return redirect('dashboard')

    context = {
        'widgets': widgets,
    }

    return render(request, 'dashboard.html', context)

@login_required
def main_app_view(request):
    """Main Snap&Report application view"""
    # Get user's reports for history
    user_reports = Report.objects.filter(generated_by=request.user).order_by('-generated_at')

    # Get recent public reports
    recent_public_reports = Report.objects.filter(is_public=True).exclude(generated_by=request.user)[:10]
    
    # Get all complaints ordered by creation date (newest first)
    complaints = Complaint.objects.all().order_by('-created_at')

    # Log app access
    UserActivity.objects.create(
        user=request.user,
        activity_type='app_access',
        description='Accessed main Snap&Report application',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    context = {
        'user': request.user,
        'user_reports': user_reports,
        'recent_public_reports': recent_public_reports,
        'complaints': complaints,
    }

    return render(request, 'main_app.html', context)

@login_required
@csrf_exempt
def submit_report(request):
    """Handle report submission from the main app"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            category = request.POST.get('category')
            description = request.POST.get('description')
            location = request.POST.get('location')

            # Create report data
            report_data = {
                'title': title,
                'category': category,
                'description': description,
                'location': location,
                'status': 'Reported',
                'likes': 0
            }

            # Handle photo upload if present
            if request.FILES.get('photo'):
                # In a real application, you'd save the file and get its URL
                report_data['photo_url'] = '/media/reports/default.jpg'

            # Create the report
            report = Report.objects.create(
                title=title,
                report_type='custom',
                data=report_data,
                generated_by=request.user,
                is_public=True
            )

            # Log the report submission
            UserActivity.objects.create(
                user=request.user,
                activity_type='report_submitted',
                description=f'Submitted report: {title}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            return JsonResponse({
                'success': True,
                'message': 'Report submitted successfully!',
                'report_id': report.id
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })

    return JsonResponse({
        'success': False,
        'message': 'Method not allowed'
    })

def get_client_ip(request):
    """Get the client IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
