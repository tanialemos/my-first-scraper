import requests
from bs4 import BeautifulSoup
import re
import json

# urls
root_url = "https://country-leaders.herokuapp.com"
status_url = root_url + "/status"
countries_url = root_url + "/countries"
cookie_url = root_url + "/cookie"
leaders_url = root_url + "/leaders"

def set_cookies() :
    cookie_request = requests.get(cookie_url)
    return cookie_request.cookies

cache = {}
def hashable_cache(f):
    def inner(url, session):
        if url not in cache:
            cache[url] = f(url, session)
        return cache[url]
    return inner

@hashable_cache
def get_first_paragraph(wikipedia_url, session):
    req = session.get(wikipedia_url)
    soup = BeautifulSoup(req.text, "html.parser")
    
    for paragraph in soup.find_all('p'):
        if paragraph.find('b') :
            first_paragraph = paragraph.text
            break
        
    square_brackets_pattern = "[\x5B]\w+[\x5D]?"
    phonetic_pattern = "\s[\x28]{1}/{1}.+/{1}.+?[\x29]{1}"
   
    para1 = re.sub(square_brackets_pattern, "", first_paragraph)
    para2 = re.sub(phonetic_pattern, "", para1)

    return para2

def get_leaders():
    
    cookies = set_cookies()
    countries = requests.get(countries_url, cookies=cookies).json()

    leaders_per_country = {}
    session = requests.Session()
    for country in countries:
        cookies = set_cookies() # cookies expire after 30sec
        leaders = requests.get(leaders_url, params={"country" : country}, cookies=cookies).json()
        for leader in leaders:
            url = leader.get('wikipedia_url')
            first_paragraph = get_first_paragraph(url, session)
            leader.update({'first_paragraph' : first_paragraph})
        leaders_per_country[country] = leaders

    return leaders_per_country

def save():
    json_file = open("leaders.json", "w")
    json_file.write(json.dumps(get_leaders()))
    json_file.close()

save()