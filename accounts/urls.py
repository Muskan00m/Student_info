from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("register", views.register, name ="register"),
    path("login", views.logins, name ="login"),
    path("dashboard", views.admin_dashboard, name ="admin-dashboard"),
    path("dashboard/profile", views.admin_profile, name ="admin-profile"),
    path("dashboard/manage-staff", views.manage_staff, name ="manage-staff"),
    path("dashboard/edit-staff/<int:id>" , views.edit_staff, name = "edit-staff"),
    path("dashboard/manage-students", views.manage_students, name ="manage-students"),
    path("dashboard/document-approval", views.document_approval, name ="document-approval"),
    path('dashboard/documents/<str:status>/', views.admin_documents_by_status, name='documents_by_status'),
    path('approve/<int:id>/', views.approve_document, name='approve_document'),
    path('reject/<int:id>/', views.reject_document, name='reject_document'),
    path('delete/<int:id>/', views.delete_user, name='delete_user'),
    path('redirect-dashboard/', views.redirect_dashboard, name='redirect-dashboard'),
]


