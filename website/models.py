from django.db import models
from django.conf import settings


# Unified category choices used by both Record and Profile
CATEGORY_CHOICES = [
    ("infrastructure", "Infrastructure"),
    ("sanitation", "Sanitation"),
    ("utilities", "Utilities"),
    ("transport", "Transport"),
    ("health_safety", "Health & Safety"),
    ("environment", "Environment"),
    ("other", "Other"),
]


class Record(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="infrastructure",
    )
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, default="medium")
    # Geolocation fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# models.py

from django.contrib.auth.models import User

class Profile(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    completed = models.BooleanField(default=False)  # track profile completion
    # Reuse the same unified set of categories
    ADMIN_CATEGORY_CHOICES = CATEGORY_CHOICES
    admin_category = models.CharField(
        max_length=50,
        choices=ADMIN_CATEGORY_CHOICES,
        default="infrastructure",
        help_text="Select your admin category to see relevant issues",
    )
    # Add other fields as needed
    def __str__(self):
        return self.user.username
