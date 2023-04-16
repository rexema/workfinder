from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from jobapp.forms import JobForm
from jobapp.models import Category, Job
from jobapp.permission import user_is_employer

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
