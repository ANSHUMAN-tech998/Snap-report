# website/middleware.py
from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from .models import Profile

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check for logged-in staff/admin users
        if request.user.is_authenticated and request.user.is_staff:
            # Ensure a Profile object exists (safe for pre-existing users)
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                Profile.objects.create(user=request.user)
                profile = request.user.profile

            if not profile.completed:
                # Try to resolve the named URL; fall back to the expected path
                try:
                    complete_url = reverse('complete_profile')
                except NoReverseMatch:
                    complete_url = '/complete-profile/'

                try:
                    logout_url = reverse('admin:logout')
                except NoReverseMatch:
                    logout_url = '/admin/logout/'

                # Avoid redirect loop (and allow logout)
                if request.path not in (complete_url, logout_url):
                    return redirect(complete_url)

        return self.get_response(request)


