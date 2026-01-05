from django.urls import path
from student import views
urlpatterns = [
    path("dashboard",views.student_dashboard ,name = "student-dashboard"),
    path("document-preview/<int:id>/",views.doucment_preview,name = "document-preview"),
    path("documents-list",views.documents_list ,name = "documents-list"),
    path("profile",views.student_profile,name = "student-profile"),
    path("upload-documents",views.upload_documents ,name = "upload-documents"),
]
