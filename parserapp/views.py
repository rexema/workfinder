from django.shortcuts import render
from parserapp.run_parser import get_links, get_data_from_link
from parserapp.models import Vacancy_Parsed


# Create your views here.
def set_parser(request):
    """
    Страница с параметрами запуска парсера
    """
    return render(request, 'parserapp/run_parser.html')

def parse_vacancy(request):

    # MAX PAGE, 1 page = 20 links
    MAX_PAGE = int(request.GET.get('max_count_vacancy'))
    if MAX_PAGE > 3:
        MAX_PAGE = 1
    # название специальности
    VACANCY_NAME = request.GET.get('specialization')

    for a in get_links(VACANCY_NAME, MAX_PAGE):
        # Создаем словарь с данными и сохраним в БД
        try:
            new_vacancy = Vacancy_Parsed(**get_data_from_link(a))  
            new_vacancy.save()
        except:
            continue
    return render(request, 'parserapp/parse_vacancy.html')


def show_vacancy(request):
    vacancy = Vacancy_Parsed.objects.all()
    return render(request, 'parserapp/show_vacancy.html', {'vacancy': vacancy})
