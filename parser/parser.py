import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

# create User Agent
UA = fake_useragent.UserAgent()

# MAX PAGE, 1 page = 20 links
MAX_PAGE = 1

VACANCY_NAME = 'python'

def get_links(text, page_count=MAX_PAGE):
    url_adress = f"https://hh.ru/search/vacancy?text={text}&salary=&area=1&ored_clusters=true&page=0"
    data = requests.get(
        url=url_adress,
        headers={"user-agent":UA.random}
        )
    if data.status_code != 200:
        # если статус запроса не равен 200 то выход
        return
    
    
    # get links
    for page in range(page_count):
        try:
            url_adress = f"https://hh.ru/search/vacancy?text={text}&salary=&area=1&ored_clusters=true&page={page}"
            data = requests.get(
                url=url_adress,
                headers={"user-agent":UA.random}
                )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"class":"serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")
        time.sleep(1)
        
    

def get_data_from_link(link):
    data = requests.get(
        url=link,
        headers={"user-agent":UA.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    
    try:
        title = soup.find(attrs={"class": "bloko-header-section-1"}).text
    except:
        title = ""
    
    try:
        salary = soup.find(attrs={"class": "bloko-header-section-2 bloko-header-section-2_lite"}).text.replace("\xa0", "")
    except:
        salary = ""

    try:
        name_company = soup.find(attrs={"class": "vacancy-company-details"}).text.replace("\xa0", " ")
    except:
        name_company = ""
    
    try:
        adress_company = soup.find(attrs={"class": "bloko-link bloko-link_kind-tertiary bloko-link_disable-visited"}).text.replace("\xa0", "")
    except:
        adress_company = "Москва"
    
    try:
        key_skills = ', '.join([tag.text for tag in soup.find(attrs={"class": "bloko-tag-list"}).find_all(attrs={"class":"bloko-tag__section_text"})]).replace("\xa0", " ")
    except:
        key_skills = "Python3"
    """
    данные для Модели Парсинга вакансий
    """
    vacancy_data = {
        "title": title,
        "salary": salary,
        "url": link,
        "name_company": name_company,
        "adress_company": adress_company,
        # "description": description,
        "key_skills": key_skills,
        }
    return vacancy_data


if __name__ == '__main__':
    data = []
    for a in get_links(VACANCY_NAME):
        data.append(get_data_from_link(a))
        time.sleep(1)
        with open("parser/vacancy_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)