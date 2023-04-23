import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

UA = fake_useragent.UserAgent()

def get_links(text, page_count=1):
    url_adress = f"https://hh.ru/search/vacancy?text={text}&salary=&area=1&ored_clusters=true&page=0"
    data = requests.get(
        url=url_adress,
        headers={"user-agent":UA.random}
        )
    if data.status_code != 200:
        # если статус запроса не равен 200 то выход
        return
    # get content
    soup = BeautifulSoup(data.content, "lxml")
    # get max page_count
    try:
        if page_count != 1:
            page_count = int(soup.find("div", attrs={"class":"pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
    except:
        return
    
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
        
    vacancy_data = {
        "title": title,
        }
    return vacancy_data


if __name__ == '__main__':
    for a in get_links('python'):
        print(get_data_from_link(a))
        time.sleep(1)