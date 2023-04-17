from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from jobapp.models import Resume
from jobapp.permission import user_is_employee
from users.forms import *


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
    messages.success(request, 'You are Successfully logged out')
    return redirect('users:login')


def resume_add(request):
    form = ResumeForm(request.POST, request.FILES)

    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()

            # for save tags
            form.save()

    context = {
        'form': form,

    }

    return render(request, 'users/employee-resume.html', context)


def show_resume(request, id):
    """
    Смотреть детали резюме
    """
    resumes = Resume.objects.filter(user_id=id)
    print(resumes)

    context = {'resume': resumes}
    return render(request, 'users/show_resumes.html', context)
