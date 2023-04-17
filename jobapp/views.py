from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from jobapp.forms import JobForm, JobApplyForm, JobEditForm
from jobapp.models import Category, Job, Applicant
from jobapp.permission import user_is_employer, user_is_employee

User = get_user_model()


def home_view(request):
    return render(request, 'jobapp/index.html')


class NewsPageView(TemplateView):
    template_name = "jobapp/news.html"
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_qs"] = News.objects.all()
        return context
    """


class AboutPageView(TemplateView):
    template_name = 'jobapp/about.html'


class ContactsPageView(TemplateView):
    template_name = 'jobapp/contacts.html'


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employer
def create_job_view(request):
    """
    Создать вакансию
    """
    form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                request, 'Вы успешно разместили свою вакансию! Пожалуйста, дождитесь рассмотрения')
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': instance.id
            }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'jobapp/post-job.html', context)


def single_job_view(request, id):
    """
    Смотреть детали вакансии
    """
    if cache.get(id):
        job = cache.get(id)
    else:
        job = get_object_or_404(Job, id=id)
        cache.set(id, job, 60 * 15)
    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list)

    }
    return render(request, 'jobapp/job-single.html', context)


def job_list_view(request):
    """
    Отобразить список вакансий
    """
    job_list = Job.objects.filter(is_published=True, is_closed=False).order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/job-list.html', context)


def search_result_view(request):
    """
    Поиск вакансий
    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/result.html', context)


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employee
def apply_job_view(request, id):
    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('users:login'))
def dashboard_view(request):
    """
    """
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs': appliedjobs,
        'total_applicants': total_applicants
    }

    return render(request, 'jobapp/dashboard.html', context)


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employer
def delete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employer
def make_complete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'Your Job was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employer
def all_applicants_view(request, id):
    all_applicants = Applicant.objects.filter(job=id)

    context = {

        'all_applicants': all_applicants
    }

    return render(request, 'jobapp/all-applicants.html', context)


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employee
def delete_bookmark_view(request, id):
    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:
        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employer
def applicant_details_view(request, id):
    applicant = get_object_or_404(User, id=id)

    context = {

        'applicant': applicant
    }

    return render(request, 'jobapp/applicant-details.html', context)


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employee
def job_bookmark_view(request, id):
    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('users:login'))
@user_is_employer
def job_edit_view(request, id=id):
    """
    Handle Job Update

    """

    job = get_object_or_404(Job, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)
