from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import School, Newjob
from teacher.models import Teacher, Application
from django.core.paginator import Paginator
from django.db.models import Count
from notification.views import create_notification 
from django.core.mail import send_mail




# school dashboard , display available teacher from the latest to join
@login_required(login_url='login-user')
def school_home(request):
    username = request.user.username       

    teachers = Teacher.objects.all().order_by('-created_at')
    try:                                                            # Attempt to retrieve the School object associated with the current user
        school = School.objects.get(user=request.user)
    except School.DoesNotExist:                                              # If the School object does not exist, redirect the user to the school_profile page
        return redirect('school_profile')

    posted_jobs = Newjob.objects.filter(school=school)

    # getting search parameters from the html
    search_location = request.GET.get('location')
    search_subject = request.GET.get('subject') 

    if search_location:
        teachers = teachers.filter(location=search_location)
    if search_subject:
        teachers = teachers.filter(subject=search_subject)

    #pagination for available teachers
    page = Paginator(teachers, 20)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {'username': username, 'page': page, 'school': school, 'posted_jobs': posted_jobs, 'search_location': search_location, 'search_subject': search_subject}
    return render(request, 'school/home.html', context)

   


# creating a school profile for the school
@login_required(login_url='login-user')
def school_profile(request):
    if request.user.is_school:
        if request.method == 'POST':
            user = request.user
            location = request.POST.get('county')
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            website = request.POST.get('website')
            description = request.POST.get('description')
            school_type = request.POST.get('schooltype')

            school = School(user=user, location=location, address=address,
                            contact=contact, description=description, website=website, school_type=school_type)
            school.save()

            if not request.user.has_school:
                request.user.has_school = True
                request.user.save()

            return redirect('school_home')

        return render(request, 'school/schoolprofile.html')




# updating the school profile 
@login_required(login_url='login-user')
def update_profile(request):
    school = request.user.school

    if request.method == 'POST':
        school.location = request.POST.get('county')
        school.address = request.POST.get('address')
        school.contact = request.POST.get('contact')
        school.website = request.POST.get('website')
        school.description = request.POST.get('description')
        school.school_type = request.POST.get('schooltype')

        school.save()
        return redirect('school_home')

    return render(request, 'school/updateprofile.html', {'school': school})





 # viewing teachers details by the school
@login_required(login_url='login-user')
def view_teacher(request):
    teacher_id = request.GET.get('teacher_id')
    teacher = get_object_or_404(Teacher, user_id=teacher_id)

    context = {'teacher': teacher}
    return render(request, 'school/viewteacher.html', context)




# view posted job by the school due to job id
@login_required(login_url='login-user')
def view_posted_jobs(request):
    job_id = request.GET.get('id')
    job = get_object_or_404(Newjob, id=job_id)

    context = {'job': job}
    return render(request, 'school/viewpostedjobs.html', context)



# adding a new job
@login_required(login_url='login-user')
def add_new_job(request):

    if request.method == 'POST':
        user = request.user            # Retrieve the school user object
        # Retrieve the associated school
        school = School.objects.get(user=user)

        subject = request.POST['subject']
        salary = request.POST['salary']
        description = request.POST['description']
        requirements = request.POST['requirements']
        qualifications = request.POST['qualifications']

        new_job = Newjob(school=school, subject=subject, salary=salary,
                         description=description, requirements=requirements, qualifications=qualifications)
        new_job.save()

    # creating an instance of posted job notification as well as sending an email to the matched teacher
        matched_teachers = Teacher.objects.filter(subject=subject)
        for teacher in matched_teachers:
            create_notification(teacher.user, 'A new job in {} has been posted.' .format(subject), subject)
            email_subject = 'A New Job Notification'
            school1 = request.user.username
            email_message = 'A new job has been posted by {}. The subject is {} and the Salary is {}. ' .format(school1, subject, salary)
            email_message += 'Click here to check more details on the job!!'
            recipient_email = teacher.user.email

            send_mail(email_subject, email_message, 'vchalloh@gmail.com',    [recipient_email])

        return redirect('school_home')
    return render(request, 'school/addnewjob.html')


# update new job 
@login_required(login_url='login-user')
def update_new_job(request):
    job_id = request.GET.get('id')
    new_job = Newjob.objects.get(id=job_id)

    if request.method == 'POST':
        new_job.subject = request.POST.get('subject')
        new_job.salary = request.POST.get('salary')
        new_job.description = request.POST.get('description')
        new_job.requirements = request.POST.get('requirements')
        new_job.qualifications = request.POST.get('qualifications')
        new_job.save()
        return redirect('school_home')

    return render(request, 'school/updatenewjob.html', {'new_job': new_job})




# delete a job in posted jobs by id
@login_required(login_url='login-user') 
def delete_job(request):
    job_id = request.GET.get('id')
    job = Newjob.objects.get(id=job_id)
    job.delete()
    return redirect('school_home')



# activating job
@login_required(login_url='login-user') 
def activate_job(request):
    job_id = request.GET.get('id')
    if job_id:
        job = Newjob.objects.get(id=job_id)
        job.is_active = True
        job.save()
    return redirect('school_home')  



# inactivating job
@login_required(login_url='login-user') 
def inactivate_job(request):
    job_id = request.GET.get('id')
    if job_id:
        job = Newjob.objects.get(id=job_id)
        job.is_active = False
        job.save()
    return redirect('school_home')



# all applicants for the school
@login_required(login_url='login-user') 
def all_applicants(request):
    school = request.user.school
    applications = Application.objects.filter(newjob__school=school).values('newjob__subject', 'newjob__school__location', 'newjob__salary').annotate(count=Count('newjob__subject'))

    context = {'applications': applications}
    return render(request, 'school/allapplicants.html', context)



@login_required(login_url='login-user') 
# applicants for a specific subject
def applicants_for_subject(request, subject):
    school = request.user.school
    applications = Application.objects.filter(newjob__school=school, newjob__subject=subject).order_by('-application_date')

    context = {'applications': applications, 'subject': subject}
    return render(request, 'school/applicantsforsubject.html', context)

















