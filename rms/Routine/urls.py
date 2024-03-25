from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Placeholder for the homepage
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('login/', views.user_login, name='login'),  # User login
    path('logout/', views.user_logout, name='logout'),  # User logout
    path('timetable/', views.view_timetable, name='view_timetable'),  # View timetable
    path('update_timetable/', views.update_timetable, name='update_timetable'),  # Update timetable
    path('alerts/', views.alerts, name='alerts'),
    path('report/',views.generate_reports,name="report")
]
