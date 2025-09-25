from django.contrib import admin

# Register your models here.
from .models import Record
admin.site.register(Record)
# to register the model in admin site so that we can add, edit, delete records from admin site
# after registering the model, we need to create a superuser to access the admin site
# we can create a superuser by running the command python manage.py createsuperuser
# after creating the superuser, we can login to the admin site by going to /admin url
# we can also customize the admin site by creating a new class and inheriting from admin.ModelAdmin
