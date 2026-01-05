from django.contrib import admin
from django.urls import path,include
from staff import views

urlpatterns = [
    path("dashboard", views.staff_dashboard, name ="dashboard"),
    path("profile", views.staff_profile, name ="profile"),
    path("add-student", views.add_student, name ="add-student"),
    path("edit-student/<int:student_id>", views.edit_student, name ="edit-student"),
    path("delete-student/<int:user_id>", views.delete_student, name ="delete-student"),
    path("all-students" , views.all_students , name = "all-students"),
    path("search-filter", views.search_filter, name ="search-filter"),
    path("update-student", views.update_student, name ="update-student"),
]


