import requests
import urllib.request
import pickle
from bs4 import BeautifulSoup
import re
import time
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

pdf_paths = 'Data'

def download_file(download_url, filename):
    try:
        response = urllib.request.urlopen(download_url)
        if response.status == 200:
            if filename[-3:] == 'pdf':
                file = open('Data/downloaded_files/'+filename, 'wb')
            else:
                file = open('Data/downloaded_files/'+filename + ".pdf", 'wb')
            file.write(response.read())
            file.close()
    except:
        pass

all_links = sum(all_links, [])
pattern = '.*(\.pdf)' 
relevant_links = []
for link in all_links:
    match = re.search(pattern, link)
    if match:
        relevant_links.append(links)

relevant_links = sum(relevant_links, [])
pattern = '[^/]+(\.pdf)'  
count = 0

for url in relevant_links:
    match = re.search(pattern, url)
    if match:
        count+=1
        title = match[0]
        download_file(url, filename=str(count)+'_'+title)
        