from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from school.models import Newjob
from django.core.paginator import Paginator
from teacher.models import Application
from django.db.models import Count





# homepage
def Homepage(request):

    jobs = Newjob.objects.all().select_related('school').order_by('-created_at')

    # get search parameters from users
    search_subject = request.GET.get('subject')
    search_location = request.GET.get('location')
    search_school_type = request.GET.get('school_type')

    #compare the value taken from select input with one in the database 
    if search_subject:
        jobs = jobs.filter(subject=search_subject)
    if search_location:
        jobs = jobs.filter(school__location=search_location)
    if search_school_type:
        jobs = jobs.filter(school__school_type=search_school_type)

    #pagination for availbale teachers
    page = Paginator(jobs, 60)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    #pass the context (page, search subject, search loaction and search school type )to the html
    context={'page':page, 'search_subject':search_subject, 'search_location':search_location, 'search_school_type':search_school_type}
    return render(request, 'users/home.html', context)




# register teacher
def RegisterTeacher(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_teacher = bool(request.POST.get('is_teacher'))

        # check whether user with same email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exits')
            return redirect('register-teacher')

        # check whether user with same username ready exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Teacher already exits')
            return redirect('register-teacher')

        # create new user
        new_user = User.objects.create_user(email=email, username=username, password=password)
        new_user.is_teacher = is_teacher
        new_user.has_resume = False
        new_user.save()

        messages.success(
            request, 'Your account has been created successfully. Please log in.')
        return redirect('login-user')

    return render(request, 'users/registerteacher.html')




# registerschool
def RegisterSchool(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_school = bool(request.POST.get('is_school'))

        # check whether the user with same email alredy exits
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exits')
            return redirect('register-school')

        # check whether school with the same username already exits
        if User.objects.filter(username=username).exists():
            messages.warning(
                request, 'School name already exits. Enter a unique school name')
            return redirect('register-school')

        # create new user
        new_user = User.objects.create_user(email=email, username=username, password=password)
        new_user.is_school = is_school
        new_user.has_school = False
        new_user.save()


        messages.success(
            request, 'Your account has been created successfully. Please log in.')
        return redirect('login-user')

    return render(request, 'users/registerschool.html')




# login
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

          # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_teacher:
                return redirect('teacher_home')
            elif user.is_school:
                    return redirect('school_home')
        else:
            messages.warning(
                request, 'Invalid Credentials. Please enter the correct username and password')

    return render(request, 'users/login.html')




# logout
def Logout(request):
    logout(request)
    return redirect('home-page')




