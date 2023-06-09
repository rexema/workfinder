import json
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from users.forms import ExperienceForm
from jobapp.models import Resume
from jobapp.permission import user_is_employee
from users.forms import *
from django.core.paginator import Paginator
import os


class ProfilePageView(TemplateView):
    template_name = "users/profile.html"


def get_success_url(request):
    """
    Handle Success Url After LogIN

    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('jobapp:home')


def employee_registration(request):
    """
    Handle Employee Registration

    """
    form = EmployeeRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('users:login')
    context = {

        'form': form
    }

    return render(request, 'users/employee-registration.html', context)


def employer_registration(request):
    """
    Handle Employee Registration

    """

    form = EmployerRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('users:login')
    context = {

        'form': form
    }

    return render(request, 'users/employer-registration.html', context)


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employee
def employee_edit_profile(request, id=id):
    """
    Handle Employee Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)
    form = EmployeeProfileEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form = form.save()
        messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse("users:edit-profile", kwargs={
            'id': form.id
        }))
    context = {

        'form': form
    }

    return render(request, 'users/employee-edit-profile.html', context)


def user_login(request):
    """
    Provides users to logIn

    """

    form = UserLoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('/')

    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))
    context = {
        'form': form,
    }

    return render(request, 'users/login.html', context)


def user_logout(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    # messages.success(request, 'You are Successfully logged out')
    return redirect('users:login')


def resume_add(request):

    form = ResumeForm(request.POST, request.FILES)
    user = get_object_or_404(User, id=request.user.id)
    
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            form.save()
            return redirect(reverse('users:show-resume', kwargs={'id': user.id }))
    context = {
            'form': form,


        }

    return render(request, 'users/employee-resume.html', context)
    

def show_resume(request, id):
    """
    Смотреть детали резюме
    """
    resumes = Resume.objects.filter(user_id=id) 
    experience = Experience.objects.filter(user_id=id)
    education = Education.objects.filter(user_id=id)   
    context = {'resume': resumes, 'experience': experience, 'education': education}
    return render(request, 'users/show_resumes.html', context)


def experience_add(request):
    form = ExperienceForm(request.POST, request.FILES)
    user = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            form.save()
            return redirect(reverse('users:show-resume', kwargs={'id': user.id }))
        else:
            messages.error(request, 'Не все поля заполнены')

    context = {
        'form': form,


    }

    return render(request, 'users/experience.html', context)


def education_add(request):
    form = EducationForm(request.POST, request.FILES)
    user = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            form.save()
            return redirect(reverse('users:show-resume', kwargs={'id': user.id }))
        else:
            messages.error(request, 'Не все поля заполнены')

    context = {
        'form': form,


    }

    return render(request, 'users/education.html', context)


def resume_list_view(request):
    """
    Отобразить список вакансий
    """
    resume_list = Resume.objects.all().order_by('-created_at')
    paginator = Paginator(resume_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'users/resume-list.html', context)


def resume_single(request, id):
    resume = Resume.objects.filter(user_id=id)
    experience = Experience.objects.filter(user_id=id)
    education = Education.objects.filter(user_id=id)
    context = {
        'resume': resume,
        'experience': experience,
        'education': education,

    }

    return render(request, 'users/single-resume.html', context)


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employee
def employee_edit_resume(request, id=id):
    """
    Handle Employee Resume Update Functionality

    """

    resume = Resume.objects.filter(user_id=id).first()
    experience =  Experience.objects.filter(user_id=id).first()
    education =  Education.objects.filter(user_id=id).first()

    if not resume:
        return redirect('users:add-resume')
    else:
        form = ResumeForm(instance=resume)
        form2 = ExperienceForm(instance=experience)
        form3 = EducationForm(instance=education)
        if request.method=='POST':
            form3 = EducationForm(request.POST,request.FILES,instance=education)
            form = ResumeForm(request.POST,request.FILES,instance=resume)
            form2 = ExperienceForm(request.POST,request.FILES,instance=experience)
            user = get_object_or_404(User, id=request.user.id)
      
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                form.save()
            if form2.is_valid:
                instance = form2.save(commit=False)
                instance.user = user
                instance.save()
                form2.save()
            if form2.is_valid:
                instance = form3.save(commit=False)
                instance.user = user
                instance.save()
                form3.save()
                    
                messages.success(request, 'Ваше резюме успешно обновлено!')
                return redirect(reverse("users:show-resume", kwargs={'id': resume.user_id }))
            else:
                messages.error(request, {request.error})
                
        context = {
                    'resume': resume,
                    'form': form,
                    'form2': form2,
                    'form3': form3
                        
                    }

        return render(request, 'users/employee-edit-resume.html', context)

        

