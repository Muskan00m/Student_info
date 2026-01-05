from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("register", views.register, name ="register"),
    path("login", views.logins, name ="login"),
    path("admin/dashboard", views.admin_dashboard, name ="admin-dashboard"),
    path("admin/profile", views.admin_profile, name ="admin-profile"),
    path("admin/manage-staff", views.manage_staff, name ="manage-staff"),
    path("admin/edit-staff/<int:id>" , views.edit_staff, name = "edit-staff"),
    path("admin/manage-students", views.manage_students, name ="manage-students"),
    path("admin/document-approval", views.document_approval, name ="document-approval"),
    path('admin/documents/<str:status>/', views.admin_documents_by_status, name='documents_by_status'),
    path('approve/<int:id>/', views.approve_document, name='approve_document'),
    path('reject/<int:id>/', views.reject_document, name='reject_document'),
    path('delete/<int:id>/', views.delete_user, name='delete_user'),
]


