from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Profile
from accounts.models import User , Profile
from staff.models import  staff
from student.models import Student
from document.models import StudentDocument
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from accounts.tasks import send_welcome_email


# Create your views here.
User = get_user_model()

def index(request):
    return render (request ,"index.html")

def register(request):
    if request.method =="POST":
        first_name = request.POST["first_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        role = request.POST["role"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]

        if password != password_confirm:
            messages.error(request , "password is not matched")
            return redirect("register")
            
        if User.objects.filter(username = username).exists():
            messages.error(request , "username is already exixts take another one ")
            return redirect("register")
        
        if User.objects.filter(email = email).exists():
            messages.error(request , "username is already exixts take another one ")
            return redirect("register")
            
        user = User.objects.create_user(
            first_name = first_name,
            username=username,
            email=email,
            role = role,
            password= password
        )
        user.save()
        send_welcome_email.delay(email, first_name)
        if role == 'staff':
            staff_data = staff.objects.get_or_create(user = user)
            return redirect("staff/dashboard")
        
        messages.success(request , "register successfully")
        return redirect("login")  
        

    else:
        return render(request ,"register.html")


def logins(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request , username = username , password = password)
        if user:

            login(request , user)

            if user.role =="admin":
                return redirect("admin-dashboard")
            elif user.role =="staff":
                return redirect("staff/dashboard")
            elif user.role =="student":
                return redirect("student/dashboard")
            else:
                messages.error(request,"invalid user")
                return redirect("login")
        else:
            messages.error(request,"invalid user")
            return redirect("login")
    else:
        return render(request , "login.html")


@login_required
def redirect_dashboard(request):
    user = request.user
    if user.role == "admin":
        return redirect("admin-dashboard")
    elif user.role == "staff":
        return redirect("staff/dashboard")
    elif user.role == "student":
        return redirect("student/dashboard")
    else:
        return redirect("login")
    

@login_required(login_url='/logins/')
def admin_dashboard(request): 
    if request.user.role != 'admin':
        messages.error(request, "Unauthorized access")
        return redirect('login')

    dashboard_data = cache.get("admin_dashboard")
    if dashboard_data is None:
        print("cache mempory")

        user = User.objects.order_by("id")[5:]
        total_student = Student.objects.all().count()
        total_staff = staff.objects.all().count()
        total_document = StudentDocument.objects.count()
        total_pending = StudentDocument.objects.filter(status = "pending").count()
        documents = StudentDocument.objects.select_related('student' , 'student__user')
        doc_map = {}
        for d in documents:
            doc_map[d.student.user_id] = d

        # 🔥 har user ke saath uska document attach karo
        for u in user:
            u.doc = doc_map.get(u.id)   # agar document nahi → None

        dashboard_data = {
            "user": user,
            "total_student": total_student,
            "total_staff": total_staff,
            "total_document": total_document,
            "total_pending": total_pending,
            "documents":documents
        }
        
        cache.set("admin_dashboard", dashboard_data, 30)
    else:
        print("redis se aaraha hai data")
    # return render(request, 'admin/dashboard.html', {"user":user , "total_student":total_student , "total_document":total_document , "total_staff":total_staff , "total_pending":total_pending })
    return render(request, "admin/dashboard.html", dashboard_data)

@login_required(login_url='/logins/')
def staff_dashboard(request):
    if request.user.role != 'staff':
        messages.error(request, "Unauthorized access")
        return redirect('login')
    return render(request, 'staff/dashboard.html')

@login_required(login_url='/logins/')
def student_dashboard(request):
    if request.user.role != 'student':
        messages.error(request, "Unauthorized access")
        return redirect('login')
    return render(request, 'student/dashboard.html')

@login_required
def admin_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST.get('phone')
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        profile.save()
        return redirect("profile")
    
    return render(request, "admin/profile.html" ,{"profile": profile})

def document_approval(request):
    document_data = cache.get("document_approval")

    if document_data is None:
        print("db data document")
        profile = Profile.objects.get(user_id = request.user.id)
        document = StudentDocument.objects.select_related('student')
        doc_pending = StudentDocument.objects.filter(status = "pending").count()
        doc_approved = StudentDocument.objects.filter(status = "approved").count()
        doc_rejected = StudentDocument.objects.filter(status = "rejected").count()
        
        document_data = {
            "profile":profile,
            "document": document,
            "doc_pending" : doc_pending,
            "doc_approved" : doc_approved,
            "doc_rejected" : doc_rejected,
        }
        cache.set("document_approval",document_data , 30)
    else:
        print("redis data")
    # return render(request , "admin/document-approval.html" , {"document":document , "profile":profile , "doc_pending":doc_pending ,"doc_approved":doc_approved, "doc_rejected":doc_rejected})
    return render(request , "admin/document-approval.html" ,document_data)

@login_required
def manage_students(request):
    profile = Profile.objects.get(user_id = request.user.id)
    student = Student.objects.select_related('user')
    documents = StudentDocument.objects.select_related('student')
    if request.method == "POST":
        full_name = request.POST["full_name"]
        course = request.POST["course"]
        status = request.POST["status"]

        if full_name:
            documents = documents.filter(student__full_name__icontains=full_name)

        if course:
            documents = documents.filter(student__course=course)

        if status:
            documents = documents.filter(status=status)
    return render(request ,"admin/manage-students.html" , {"student":student ,"documents":documents , "profile":profile})

@login_required
def manage_staff(request):
    profile = Profile.objects.get(user_id = request.user.id)
    # user = staff.objects.select_related('staff_info')
    staff_info = staff.objects.select_related('user')
    return render(request,"admin/manage-staff.html", {"staff_info":staff_info , "profile":profile} )

def edit_staff(request , id):
    staff_data = get_object_or_404(staff ,user_id = id)
    user_data = get_object_or_404(User , id = id)
    profile = get_object_or_404(Profile , user_id = id)
    if request.method == "POST":

        if(profile.photo):
            profile.phone = request.POST.get('phone')
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            profile.save()

        profile.phone = request.POST['phone']
        profile.save()

        staff_data.department = request.POST["department"]
        staff_data.address = request.POST["address"]
        staff_data.save()
        return redirect("edit-staff", id=staff_data.user_id)
    
    return render(request , "admin/edit-staff.html", {"staff_data":staff_data , "user_data":user_data , "profile":profile})


def approve_document(request, id):

    doc = get_object_or_404(StudentDocument, id=id)

    # document approved
    doc.status = 'approved'
    doc.save()

    # student approved
    student = Student.objects.get(id = doc.student_id)
    student.approved = True
    student.save()

    return redirect("document-approval")


def reject_document(request, id):

    doc = get_object_or_404(StudentDocument, id=id)

    doc.status = 'rejected'
    doc.save()

    # student approved false hi rahega
    student = Student.objects.get(id = doc.student_id)
    student.approved = False
    student.save()

    return redirect("document-approval")


def admin_documents_by_status(request, status):

    documents = StudentDocument.objects.filter(status=status).select_related('student')

    return render(request,'admin/all-documents.html',{ 'documents': documents, 'status': status })

def delete_user(request , id):
    user = get_object_or_404(User , id=id , role ="staff" )
    user.delete()
    profile = Profile.objects.get(user_id = request.user.id)
    staff_info = staff.objects.select_related('user')
    return render(request  , "admin/manage-staff.html",  {"staff_info":staff_info ,"profile":profile})

@login_required
def delete_student(request , user_id):
    user = get_object_or_404(User , id=user_id , role ="student" )
    user.delete()
    staff_info = staff.objects.select_related('user')
    return render(request , "admin/all-students.html",{"staff_info":staff_info })


def cache_test(request):
    cache.set("test_key", "Hello Momo", timeout=60)
    value = cache.get("test_key")
    return HttpResponse(value)

