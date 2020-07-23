#Load the relevant python libraries
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import pandas as pd

import urllib
import requests
from requests.exceptions import RequestException
from urllib.request import HTTPError
from urllib.request import urlopen

import bs4
import re
from socket import timeout


import os
import random


#load the dataframe and save to folder paths

DF = pd.read_excel("C:\\Users\\amarti32\\Desktop\\BigQueryResults2\\BigQueryResults_Original.xlsx")

Save2017 = "C:\\Users\\amarti32\\Desktop\\URLSwith2017"
Saveno2017 = "C:\\Users\\amarti32\\Desktop\\URLSwithot2017"

#define a function to store the URLS into a list

def URLLister(dataframe):
    URLS = []
    for i in dataframe["Did"]:
        URLS.append(i)
    
    return URLS


#define function that checks each url for keyword and saves to a specified folder
def URLOpenAndSave(URLS):
    search_word = "2017"
    hdrs = {'User-Agent': 'Mozilla / 5.0 (X11 Linux x86_64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36'}
    
    try:
        print("Searching article:",)
        response = requests.get(URLS, headers=hdrs, timeout = 2.5)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        results = soup.find_all(string=re.compile('.*{0}.*'.format(search_word)), recursive=True)
        print('Found the word "{0}" {1} times in article'.format(search_word, len(results)))
        
        if len(results) == 0:
            num = random.random()
            print("2017 NOT found in article")
            page = urllib.request.urlopen(URLS, timeout = 2.5)
            content = page.read()
            outFile = open(os.path.join(Saveno2017,"Article_"+str(num)+".html"),"wb")
            outFile.write(content)
            outFile.close()
            print("Article written to SaveNo2017 folder\n")
            
        else:
            num = random.random()
            print("2017 found in article")
            page = urllib.request.urlopen(URLS, timeout = 2.5)
            content = page.read()
            outFile = open(os.path.join(Save2017,"Article_"+str(num)+".html"),"wb")
            outFile.write(content)
            outFile.close()
            print("Article written to Save2017 folder\n")
                
                
    except (Exception, RequestException, urllib.error.URLError, urllib.error.HTTPError, timeout, TimeoutError) as err:
        print("Error with request\n")
        pass


if __name__ == '__main__':
    
    urls = URLLister(DF)
    
    pool = Pool()
    print("Beginning scraping of URLs...\n")
    
    pool.map(URLOpenAndSave, urls)
    pool.close()
    print("No more work submitted to pool instance")
    pool.join()
    
    print("URLs Scraped and Finished")
























