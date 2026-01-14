from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate,login
from django.contrib.auth.decorators import login_required
from accounts.models import User , Profile
from staff.models import  staff
from student.models import Student
from document.models import StudentDocument
from accounts.tasks import send_notification_email

# Create your views here.
@login_required(login_url='/logins/')
def staff_dashboard(request):
    token = request.session.get('access_token')
    print("JWT TOKEN - token is created")
    
    if not token:
        print("Token is expired ❌")
        return redirect("login")
    
    if request.user.role != 'staff':
        messages.error(request, "Unauthorized access")
        return redirect('login')
    
    student = Student.objects.order_by("-id")[:3]
    total_student = Student.objects.all().count() 
    total_staff = staff.objects.all().count()
    total_pending = StudentDocument.objects.filter(status = "pending").count()
    total_document = StudentDocument.objects.all().count()
    return render(request, 'staff/dashboard.html', {"student":student , "total_student":total_student , "total_staff":total_staff , "total_pending":total_pending , "total_document":total_document})


@login_required
def staff_profile(request):
    staff_data= staff.objects.get(user_id=request.user.id)
    profile, created = Profile.objects.get_or_create(user=request.user)
    user_data = request.user
    # staff_data = staff.objects.get(user = request.user)
    if request.method == "POST":
        profile.phone = request.POST.get('phone')
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        profile.save()

        staff_data.department = request.POST['department']
        staff_data.address = request.POST['address']
        staff_data.save()

        send_notification_email.delay(
        "update profile",
        "Your profile has been uploaded.",
        user_data.email
        )

        return redirect("profile")
    
    return render(request, "staff/profile.html" ,{"profile": profile , "staff_data":staff_data, "user_data":user_data})

@login_required
def add_student(request):
    if request.method == "POST":
        try:
            full_name = request.POST["full_name"]
            email = request.POST["email"]
            username = request.POST["username"]
            password = request.POST["password"]
            re_password = request.POST["re-password"]
            role = "student"

            if password != re_password:
                messages.error(request , "password is not matched")
                return redirect("add-student")

            if User.objects.filter(username = username).exists():
                messages.error(request , "username is already exixts take another one ")
                return redirect("add-student")

            if User.objects.filter(email = email).exists():
                messages.error(request , "username is already exixts take another one ")
                return redirect("add-student")
                

            user = User.objects.create_user(password = password , username = username ,
                                                first_name = full_name , email = email , 
                                                role = role
                                                )
            user.save()

            roll_number = request.POST["roll_number"]
            phone = request.POST["phone"]
            date_of_birth = request.POST["date_of_birth"]
            gender = request.POST["gender"]
            course = request.POST["course"]
            year = request.POST["year"]
            semester = request.POST["semester"]
            address = request.POST["address"]
            guardian_name = request.POST["guardian_name"]
            guardian_phone = request.POST["guardian_phone"]

            student = Student.objects.create(user = user,
                                                full_name = full_name , email = email,
                                                roll_number = roll_number,
                                                phone = phone , date_of_birth = date_of_birth ,
                                                gender = gender , course = course , year = year ,
                                                semester = semester , address = address , 
                                                guardian_name = guardian_name , guardian_phone = guardian_phone
                                                )
            student.save()
            send_notification_email.delay(
            "created profile",
            " welcome... Your profile has been created .",
            user.email
            )
            messages.success(request, "Student created successfully")
            return redirect("dashboard")
        
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("add-student")
    else :
        return render(request , "staff/add-student.html")

@login_required
def edit_student(request , student_id):
    user = get_object_or_404(User, id= student_id, role='student')
    student =  get_object_or_404(Student , user_id=student_id )
    print(student.user_id)
    print(student_id)

    if request.method == "POST":
        full_name = request.POST["full_name"]
        phone = request.POST["phone"]
        date_of_birth = request.POST["date_of_birth"]
        gender = request.POST["gender"]
        course = request.POST["course"]
        year = request.POST["year"]
        semester = request.POST["semester"]
        address = request.POST["address"]
        guardian_name = request.POST["guardian_name"]
        guardian_phone = request.POST["guardian_phone"]


        student.full_name = full_name
        student.phone = phone
        student.address = address
        student.date_of_birth = date_of_birth
        student.gender = gender
        student.course = course
        student.year = year
        student.semester = semester
        student.guardian_name = guardian_name
        student.guardian_phone = guardian_phone
        student.save()
        send_notification_email.delay(
            "update profile",
            " welcome... Your profile has been updated .",
            student.email
            )

        full_name = request.POST["full_name"]
        user.first_name = full_name
        user.save()
        return redirect("dashboard")

    return render(request , "staff/edit-student.html" , {"user":user,"student":student})

@login_required
def all_students(request):
    # student = User.objects.filter(role ="student")
    student = Student.objects.all()
    profile  = Profile.objects.get(user_id = request.user.id)
    return render(request , "staff/all-students.html", {"student":student , "profile":profile})

@login_required
def delete_student(request , user_id):
    user = get_object_or_404(User , id=user_id , role ="student" )
    user.delete()
    send_notification_email.delay(
            "delete account",
            " your account has been deleted.",
            user.email
            )
    return render(request , "staff/all-students.html",)

@login_required
def search_filter(request):
    profile = Profile.objects.get(user_id = request.user.id)
    documents = StudentDocument.objects.select_related('student')
    if request.method == "POST":
        full_name = request.POST["full_name"]
        roll_number = request.POST["roll_number"]
        course = request.POST["course"]
        status = request.POST["status"]

        if full_name:
            documents = documents.filter(student__full_name__icontains=full_name)

        if roll_number:
            documents = documents.filter(student__roll_number__icontains=roll_number)

        if course:
            documents = documents.filter(student__course=course)

        if status:
            documents = documents.filter(status=status)
        
        return render( request ,"staff/search-filter.html" , {"documents":documents , "profile":profile})


    return render(request, "staff/search-filter.html", {"profile":profile})

@login_required
def update_student(request):
    return render (request , "staff/update-student.html")
