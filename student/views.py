from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from student.models import Student
from accounts.models import User , Profile
from document.models import StudentDocument

# Create your views here.
@login_required(login_url='/logins/')
def student_dashboard(request):
    if request.user.role != 'student':
        messages.error(request, "Unauthorized access")
        return redirect('login')
    student = Student.objects.get(user=request.user)
    document = StudentDocument.objects.filter(student = student).count()
    document_approved = StudentDocument.objects.filter(student= student ,status = "approved").count()
    document_rejected = StudentDocument.objects.filter(student = student , status = "rejected").count()
    document_pending = StudentDocument.objects.filter(student = student ,status = "pending").count()
    document_total = StudentDocument.objects.filter(student= student)
    
    return render(request,"student/dashboard.html" ,{"document":document , "document_pending":document_pending ,"document_approved":document_approved , "document_rejected":document_rejected , "document_total":document_total})

@login_required
def doucment_preview(request, id ):
    document = get_object_or_404(StudentDocument , id = id)
    print(id)
    print(document.id)
    profile  = Profile.objects.get(user_id = request.user.id)
    return render(request, "student/document-preview.html", {"document":document , "profile":profile})


@login_required
def student_profile(request):
    stud = Student.objects.get(user = request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile = Profile.objects.get(user = request.user)

    if request.method == "POST":
        stud.full_name = request.POST["full_name"]
        stud.phone = request.POST["phone"]
        stud.gender = request.POST["gender"]
        stud.course = request.POST["course"]
        stud.year = request.POST["year"]
        stud.semester = request.POST["semester"]
        stud.address = request.POST["address"]
        stud.guardian_name = request.POST["guardian_name"]
        stud.guardian_phone = request.POST["guardian_phone"]
        stud.save()
        
        profile.phone = request.POST.get('phone')
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        profile.save()
        
        return redirect("student-profile")
    return render(request, "student/profile.html" , {"stud":stud , "profile":profile})


@login_required
def documents_list(request):
    student = Student.objects.get(user=request.user)
    doc = StudentDocument.objects.filter(student = student)
    pending= StudentDocument.objects.filter(student =student , status = "pending")
    approved= StudentDocument.objects.filter(student =student ,status = "approved")
    reject= StudentDocument.objects.filter(student =student ,status = "rejected")
    p1= StudentDocument.objects.filter(student =student , status = "pending").count()
    a1= StudentDocument.objects.filter(student =student ,status = "approved").count()
    r1= StudentDocument.objects.filter(student =student ,status = "rejected").count()
    d1 = StudentDocument.objects.filter(student = student).count()
    profile  = Profile.objects.get(user_id = request.user.id)
    return render(request, "student/documents-list.html",{"doc":doc , "pending":pending ,"approved":approved , "reject":reject , "p1":p1 , "a1":a1,"r1":r1, "d1":d1 , "profile":profile})

@login_required
def upload_documents(request):
    student = Student.objects.get(user =request.user)
    if request.method == "POST":
        title = request.POST['title']
        doc = request.FILES['doc']
        discrip= request.POST['discrip']
        document = StudentDocument.objects.create(student= student ,title=title , doc = doc, discrip= discrip)
        document.save()
        messages.success(request, "Document uploaded successfully")
        return redirect("student-dashboard")
    profile  = Profile.objects.get(user_id = request.user.id)

    return render(request, "student/upload-documents.html",{"profile":profile})
