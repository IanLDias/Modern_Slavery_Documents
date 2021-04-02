import requests
import pickle
from bs4 import BeautifulSoup
import re
query = 'modern slavery statements pdf'
query = query.replace(' ', '+')

all_links = []
for page_number in range(0, 500,10):
    url = f"https://google.com/search?q={query}&start={page_number}'"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")   
    result = soup.find_all('div', attrs = {'class': 'ZINbbc'})
    results=[re.search('\/url\?q\=(.*)\&sa',str(i.find('a', href = True)['href'])) for i in result if "url" in str(i)]
    #this is because in rare cases we can't get the urls
    links=[i.group(1) for i in results if i != None]
    all_links.append(links)

with open("statementurls.txt", "wb") as f:
    pickle.dump(all_links, f)