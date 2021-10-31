#Akash Kathiari
#Web Crawler resubmission
#IS 392

                    ### import packages ###
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os

                    ### set up SSL Enviorment ###
try:
        _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
        pass
else:
        ssl._create_default_https_context = _create_unverified_https_context

                    ### get page content ###
def get_page_content(url):
    try:
        html_response_text = urlopen(url).read()
        page_content = html_response_text.decode('utf-8')
        return page_content
    except Exception as e:
        return None

                    ### parse page content using BeautifulSoup ###
#def parse_page_content(page_content):
        #soup = BeautifulSoup(page_content, 'html.parser')
        #page_text = soup.get_text()
        #title = soup.title.string
        #title = clean_title(title)

                    ### clean the title of the page ###
def clean_title(title):
        invalid_characters = ['>','<',':','"','/','\\','?','*']
        for c in invalid_characters:
            title = title.replace(c, ' ')
        return title

                    ### extract outgoing(inner) Urls from page content ###
def get_url(soup):
        links = soup.find_all('a')
        urls = []
        for link in links:
                urls.append(link.get('href'))
        return urls

                    ### check if a url is valid ###
def is_url_valid(url):
        if url is None:
                return False
        if re.search('#', url):
                return False
        match=re.search('^/wiki/', url)
        if match:
                return True
        else:
                return False

                    ###  reformat url, change a relative url into  full url ###
def reformat_url(url):
        match=re.search('^/wiki/',url)
        if match:
                return "https://en.wikipedia.org" + url
        else:
                return url

                    ### save a page ###
destination_folder = "./path"        
def save(text, path):
        f = open(path,'w', encoding = 'utf-8', errors = 'ignore')
        f.write(text)
        f.close()

                    ### save crawled urls ###
def save_crawled_urls():


#Pseudo    code   of a  focused    crawler ###

    queue = []
    visitedUrlList = []                        #   prevent    a single url from entering the queue repeatedly
    pageCounter = 0
    savedUrlList = []
    relatedTerms = ['Nintendo','Mario', 'Donkey Kong', 'Link', 'Multiplayer', 'Yoshi', 'Kirby', 'Fox','Masahiro Sakurai','GameCube']
    seedUrls = ['https://en.wikipedia.org/wiki/Super_Smash_Bros','https://en.wikipedia.org/wiki/Super_Smash_Bros._Melee']

    for url in seedUrls:
        queue.append(url)
        visitedUrlList.append(url)

    while queue:

        url = queue.pop(0)
        page_content = get_page_content(url)
        soup = BeautifulSoup(page_content, 'html.parser')
        page_text = soup.get_text()

        termCounter = 0

        for term in relatedTerms:
            if re.search(term,page_content, re.I):  #  if the page contains the term
                termCounter += 1
                if termCounter >= 2:            #  if a page is topical relevant
                    title = soup.title.string
                    title = clean_title(title)
                    file_path = os.path.join(destination_folder, title + '.html')
                    save(page_content, file_path)
                    savedUrlList.append(url)
                    pageCounter += 1
                    print ('page {}: {}'.format(pageCounter, url))  #  print  information
                    break
        if pageCounter >= 501:
            break
        inner_urls = get_url(soup)
        for inner_url in inner_urls:
            if is_url_valid(inner_url):
                inner_url = reformat_url(inner_url)
                if inner_url not in visitedUrlList:
                    queue.append(inner_url)
                    visitedUrlList.append(inner_url)


        f = open("crawled_urls.txt","w")
        i = 1
        for url in savedUrlList:
            f.write(str(i) + ': ' + url + '\n')
            i += 1
        f.close()


save_crawled_urls()
