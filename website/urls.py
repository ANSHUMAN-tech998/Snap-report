from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    # Admin URLs (changed from /admin/ to /management/ to avoid conflicts)
    #path('management/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('issues/', views.issues_list, name='issues_list'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('issues/<int:issue_id>/', views.manage_issue, name='manage_issue'),
    path('report/', views.report_issue, name='report_issue'),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
     path('complete-profile/', views.complete_profile, name='complete_profile'),
     

]