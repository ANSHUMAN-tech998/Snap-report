from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm
from .models import Record, CATEGORY_CHOICES
from .forms import ProfileForm

# Create your views here.
def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # Only allow admin login
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect("admin_dashboard")  # redirect admin to dashboard
            else:
                messages.error(request, "You are not authorized to log in as admin.")
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("home")
    else:
        return render(request, "home.html")


# views.py


def complete_profile(request):
    profile = request.user.profile
    if profile.completed:
        return redirect("admin_dashboard")  # ✅ already completed → go to admin

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.completed = True
            profile.save()
            return redirect("admin_dashboard")  # ✅ after completing → admin dashboard
    else:
        form = ProfileForm(instance=profile)

    return render(request, "complete_profile.html", {"form": form})


def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "You are not authorized to view this page")
        return redirect("home")

    # Ensure profile exists and is completed (admin category selected)
    try:
        profile = request.user.profile
    except Exception:
        profile = None

    if not profile or not getattr(profile, "completed", False):
        messages.warning(request, "Please complete your profile to select your admin category.")
        return redirect("complete_profile")

    # Filter records by admin's category
    category = getattr(profile, "admin_category", "other")
    records = Record.objects.filter(category=category)

    context = {
        "total_issues": records.count(),
        "pending_issues": 0,
        "resolved_issues": 0,
        "users_count": User.objects.count(),
        "admin_category": category,
    }

    return render(request, "admin_dashboard.html", context )


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Grant admin access so they can view the dashboard immediately
            user.is_staff = True
            user.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # Ensure a Profile exists for this user (to capture admin category)
            try:
                from .models import Profile
                Profile.objects.get_or_create(user=user)
            except Exception:
                pass
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Registered successfully")
            return redirect("admin_dashboard")
        else:
            return render(request, "register.html", {"form": form})
    else:
        form = SignupForm()
        return render(request, "register.html", {"form": form})


def issues_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view issues")
        return redirect("home")

    # Filter by admin's category if staff
    if request.user.is_staff:
        try:
            category = request.user.profile.admin_category
            issues = Record.objects.filter(category=category)
        except Exception:
            issues = Record.objects.none()
            messages.warning(request, "Please complete your profile to set admin category.")
    else:
        # For non-staff, show all issues or adjust as needed
        issues = Record.objects.all()

    context = {
        "issues": issues,
        "filter_category": request.GET.get("category", ""),
        "filter_status": request.GET.get("status", ""),
    }

    return render(request, "issues_list.html", context)


from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
import json


def analytics_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view analytics")
        return redirect("home")

    # Get all records for analytics
    records = Record.objects.all()

    # Basic statistics
    total_issues = records.count()
    users_count = User.objects.count()

    # Location-based analytics (State distribution)
    state_distribution = (
        records.values("state").annotate(count=Count("state")).order_by("-count")[:10]
    )

    # City-based analytics
    city_distribution = (
        records.values("city").annotate(count=Count("city")).order_by("-count")[:10]
    )

    # Monthly trends (Records created by month)
    monthly_trends = (
        records.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")[:12]
    )

    # Contact method analytics (Email vs Phone presence)
    contact_stats = {
        "with_email": records.filter(email__isnull=False).count(),
        "with_phone": records.filter(phone__isnull=False).count(),
        "with_both": records.filter(email__isnull=False, phone__isnull=False).count(),
        "with_address": records.filter(address__isnull=False).count(),
    }

    # Convert data to JSON for JavaScript
    location_data = {}
    for item in state_distribution:
        if item["state"]:
            location_data[item["state"]] = item["count"]

    # If no state data, use city data
    if not location_data and city_distribution:
        for item in city_distribution:
            if item["city"]:
                location_data[item["city"]] = item["count"]

    # Monthly data for trends
    monthly_labels = []
    monthly_values = []
    for trend in monthly_trends:
        if trend["month"]:
            monthly_labels.append(trend["month"].strftime("%b %Y"))
            monthly_values.append(trend["count"])

    context = {
        "total_issues": total_issues,
        "resolved_this_month": records.filter(
            created_at__month=timezone.now().month
        ).count(),
        "average_resolution_time": 0,  # Not applicable for customer records
        "users_count": users_count,
        "location_data": json.dumps(location_data),
        "monthly_labels": json.dumps(monthly_labels),
        "monthly_values": json.dumps(monthly_values),
        "contact_stats": contact_stats,
        "state_distribution": state_distribution,
        "city_distribution": city_distribution,
    }

    return render(request, "analytics.html", context)


def manage_issue(request, issue_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to manage issues")
        return redirect("home")

    # Placeholder for issue management
    try:
        issue = Record.objects.get(id=issue_id)
        context = {
            "issue": issue,
            "staff_members": User.objects.filter(is_staff=True),
        }
    except Record.DoesNotExist:
        context = {
            "issue": None,
            "staff_members": User.objects.filter(is_staff=True),
        }

    return render(request, "manage_issue.html", context)


def report_issue(request):
    if request.method == "POST":
        try:
            # Get form data
            title = request.POST.get("title", "")
            description = request.POST.get("description", "")
            category = request.POST.get("category", "infrastructure")
            location = request.POST.get("location", "")
            priority = request.POST.get("priority", "medium")
            reporter_name = request.POST.get("reporter_name", "")
            reporter_email = request.POST.get("reporter_email", "")
            reporter_phone = request.POST.get("reporter_phone", "")
            latitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")

            # Validate required fields
            if not all([title, description, location, reporter_name, reporter_email]):
                messages.error(request, "Please fill in all required fields.")
                return render(request, "report_issue.html", {})

            # Convert coordinates to float if provided
            lat_value = None
            lng_value = None
            if latitude and longitude:
                try:
                    lat_value = float(latitude)
                    lng_value = float(longitude)
                except (ValueError, TypeError):
                    lat_value = None
                    lng_value = None

            # Validate category against allowed choices
            allowed_categories = {key for key, _ in CATEGORY_CHOICES}
            cat_value = category if category in allowed_categories else "infrastructure"

            # Create new record
            record = Record.objects.create(
                first_name=reporter_name.split()[0] if reporter_name else "",
                last_name=(
                    " ".join(reporter_name.split()[1:])
                    if len(reporter_name.split()) > 1
                    else ""
                ),
                email=reporter_email,
                phone=reporter_phone,
                address=location,
                city="",
                state="",
                zipcode="",
                latitude=lat_value,
                longitude=lng_value,
                category=cat_value,
                description=description,
                priority=priority,
            )

            messages.success(
                request, f"Issue reported successfully! Record ID: {record.id}"
            )
            return redirect("home")

        except Exception as e:
            messages.error(request, f"Error creating record: {str(e)}")
            return render(request, "report_issue.html", {})

    return render(request, "report_issue.html", {})
