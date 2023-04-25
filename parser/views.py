from django.shortcuts import render
from parser.parser import run_parser

# Create your views here.
def set_parser(request):
    context = {}
    return render(request, 'parser/run_parser.html', context)

def show_vacancy(request):

    # MAX PAGE, 1 page = 20 links
    MAX_PAGE = int(request.GET.get('max_count_vacancy'))
    if MAX_PAGE > 3:
        MAX_PAGE = 1
    
    # название специальности
    VACANCY_NAME = request.GET.get('specialization')

    # print(type(VACANCY_NAME), type(MAX_PAGE))
    run_parser(VACANCY_NAME, MAX_PAGE)
    
    context = {}
    return render(request, 'parser/show_vacancy.html', context)
    
