import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from school.models import Newjob
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import calendar
from teacher.models import Application

from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from intasend import APIService




token = "ISSecretKey_test_51fcb535-e653-46aa-8484-61b089b30bfc"
publishable_key = "ISPubKey_test_6cdb65b0-a6df-45db-bc60-22fa01987909"
service = APIService(token=token, publishable_key=publishable_key, test=True)





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



#delete user
def delete_user(request):
    user_id = request.GET.get('id')
    user1 = get_object_or_404(User, id=user_id)
    user1.delete()
    return redirect('home-page')

    
#view monthly reports
@login_required
@staff_member_required
def reports(request):

    if request.method == 'POST':
        date = request.POST.get('date')
    else:
        date = datetime.now().strftime('%Y-%m')    # Set the default value to the current month
        
    month1 = int(date.split('-')[1])
    year1 = int(date.split('-')[0])

    month2 = calendar.month_name[month1]


    teacher1 = User.objects.filter(is_teacher=True)
    teachers_created_this_month = []
    for teach in teacher1:  
        if teach.created_at.date().month == month1 and teach.created_at.date().year == year1:
            teachers_created_this_month.append(teach.teacher)
            
            
    job1 = Newjob.objects.filter()
    jobs_created_month = []
    for job2 in job1:
        if job2.created_at.date().month == month1 and job2.created_at.date().year == year1:
            jobs_created_month.append(job2)

        
    month_app = []
    applications = Application.objects.all()
    for app in applications:
        if app.application_date.date().month == month1 and app.application_date.date().year == year1 :
            month_app.append(app)


    context ={'teachers_created_this_month':teachers_created_this_month, 'jobs_created_month':jobs_created_month,  'month2':month2, 'year1': year1, 'month_app':month_app, 'date':date}
    return render(request, 'users/reports/reports.html', context)



# generate pdf report
@login_required
@staff_member_required
def pdf_report_create(request):
    if request.method == 'POST':
        date = request.POST.get('date')
    else:
        date = datetime.now().strftime('%Y-%m')    # Set the default value to the current month
        
    month1 = int(date.split('-')[1])
    year1 = int(date.split('-')[0])

    month2 = calendar.month_name[month1]


    teacher1 = User.objects.filter(is_teacher=True)
    teachers_created_this_month = []
    for teach in teacher1:  
        if teach.created_at.date().month == month1 and teach.created_at.date().year == year1:
            teachers_created_this_month.append(teach.teacher)
            
            
    job1 = Newjob.objects.filter()
    jobs_created_month = []
    for job2 in job1:
        if job2.created_at.date().month == month1 and job2.created_at.date().year == year1:
            jobs_created_month.append(job2)
            
       
    month_app = []
    applications = Application.objects.all()
    for app in applications:
        if app.application_date.date().month == month1 and app.application_date.date().year == year1 :
            month_app.append(app)

    template_path = 'users/reports/pdfreport.html'
    context ={'teachers_created_this_month':teachers_created_this_month, 'jobs_created_month':jobs_created_month,  'month2':month2, 'year1': year1, 'month_app':month_app}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+ month2 +' reports.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    

# def pay(request):

#     response = service.collect.mpesa_stk_push(phone_number= '254703156845', email='vchalloh@gmail.com', amount=1, narrative='purchase')

#     print(response)
#     invoice_id = response['invoice']['invoice_id']
#     phone_number = response['customer']['phone_number']

#     print('invoice_id:', invoice_id)
#     print('phone_number:', phone_number)


#     return render(request, 'users/pay.html')


def update_user_paid_status(request):
    bd=request.body
    data = json.loads(bd) 
    user_id = data['id']
    print(user_id)
    
    user = User.objects.get(id=user_id)
    print(user)
    user.has_paid = True
    user.save()
    return JsonResponse({'status': 'success'})





