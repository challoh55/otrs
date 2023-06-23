from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Teacher, Application
from school.models import Newjob
from django.core.paginator import Paginator
from django.contrib import messages
from notification.models import Postedjobs




# teacher dashboard: searching pagination and username display
@login_required(login_url='login-user') 
def teacher_home(request):
    username = request.user.username
    
    # filters jobs based on subject, location and school_type
    jobs = Newjob.objects.all().select_related('school').order_by('-created_at')
    
    # getting the search parameters from the form
    search_subject = request.GET.get('subject')
    search_location = request.GET.get('location')
    search_school_type = request.GET.get('school_type')

    if search_subject:
        jobs = jobs.filter(subject=search_subject)
    if search_location:
        jobs = jobs.filter(school__location=search_location)
    if search_school_type:
        jobs = jobs.filter(school__school_type=search_school_type)

    page = Paginator(jobs, 60)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context={'username':username, 'page':page, 'search_subject':search_subject, 'search_location':search_location, 'search_school_type':search_school_type}
    return render(request, 'teacher/home.html', context)




# creatting a resume for teacher
@login_required(login_url='login-user')
def Resume(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user

            fname = request.POST['fname']
            lname = request.POST['lname']
            phonenumber = request.POST['phonenumber']
            subject = request.POST['subject']
            location = request.POST['location']
            idnumber = request.POST['idnumber']
            dob = request.POST['dob']
            gender = request.POST['gender']
            description = request.POST['description']


            image = request.FILES['image']
            resume = request.FILES['resume']

            teacher = Teacher(user=user, fname=fname, lname=lname, phonenumber=phonenumber, subject=subject,
                            location=location, idnumber=idnumber, dob=dob, gender=gender, description=description, image=image, resume=resume)
            teacher.save()

            if not user.has_resume and user.is_teacher:
                user.has_resume = True
                user.save()

            return redirect('teacher_home')

        return render(request, 'teacher/teacherresume.html')
    return redirect('login-user')



# updating teacher resume
@login_required(login_url='login-user')
def update_resume(request):
    teacher = request.user.teacher

    if request.method == 'POST':
        teacher.fname = request.POST['fname']
        teacher.lname = request.POST['lname']
        teacher.phonenumber = request.POST['phonenumber']
        teacher.subject = request.POST['subject']
        teacher.location = request.POST['location']
        teacher.idnumber = request.POST['idnumber']
        teacher.dob = request.POST['dob']
        teacher.gender = request.POST['gender']
        teacher.description = request.POST['description']

        if 'image' in request.FILES:
            teacher.image = request.FILES['image']

        if 'resume' in request.FILES:
            teacher.resume = request.FILES['resume']

        teacher.save()
        return redirect('teacher_home')

    return render(request, 'teacher/updateresume.html', {'teacher': teacher})






# teachers viewing jobs and school and applying for the job
@login_required(login_url='login-user')     # checks if the user is authenticated if not redirects them to login page
def view_job(request):
    job_id = request.GET.get('id')
    job = get_object_or_404(Newjob, id=job_id)
    school = job.school

    # checking if the user is a teacher and if the user has already applied for the job
    user = request.user
    has_applied = Application.objects.filter(teacher=user, newjob=job).exists()

    #once teacher views job is_read field is turned to true hence notification is not dislayed in the teachers notifications anymore
    subject_notification = Postedjobs.objects.filter(subject=job, recipient=user)
    subject_notification.update(is_read=True)

    if request.method == 'POST':
        if  has_applied:
            messages.warning(request, 'You have already applied for this job')
        else:
            application = Application(newjob=job, teacher=user)
            application.save()
            messages.success(request, 'Thank you for applying this job. We will contact you as soon we get your application')


    context = {'job': job, 'school':school, 'has_applied':has_applied}
    return render(request, 'teacher/viewjob.html', context)







# applied jobs 
@login_required(login_url='login-user') 
def applied_jobs(request):
    user = request.user
    applied_jobs = Application.objects.filter(teacher=user).select_related('newjob', 'teacher').order_by('-application_date')
    context = {'applied_jobs':applied_jobs}
    return render(request, 'teacher/appliedjobs.html', context)