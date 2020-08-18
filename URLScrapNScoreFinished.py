#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Load the relevant python libraries

import arcpy
from arcpy import env
import pandas as pd
import urllib
import requests
import openpyxl as opxl
from openpyxl import Workbook
from bs4 import BeautifulSoup as bs
import traceback
import os


# In[2]:


def Table(filepath, tableName):
    table = str(filepath) + str(tableName)
    return table

def SearchTerms(filepath, FileName):
    searchFile = str(filepath) + str(FileName)
    searchDF = pd.read_excel(searchFile)
    
    "Load the search terms and turn into a dictionary"
    t6 = list()
    t7 = list()

    for i in searchDF["Term"]:
        t6.append(i)
    for j in searchDF["Score"]:
        t7.append(int(j))

    SearchTermDict = dict(zip(t6,t7))

    KeysList = list()

    for i in SearchTermDict.keys():
        KeysList.append(i)    
        
    return KeysList,SearchTermDict



def URLScrapeNScore(Table,Fields,Keyslist,SearchDict,save_folder):
    with arcpy.da.UpdateCursor(Table,Fields) as cursor:
        count = 0
        hdrs = {'User-Agent': 'Mozilla / 5.0 (X11 Linux x86_64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36'}
        for row in cursor:
            URL = row[1]
            myScore = 0
            #print(URL)
            try:
                myScore = 0
                resp = requests.get(URL,headers=hdrs,timeout=5)
                soup = bs(resp.content)
                body = soup.find('body')
                bodyp = body.find_all('p')
                for p in bodyp:
                    pToString = str(p)
                    for word in pToString.split(" "):
                        for key in Keyslist:
                            if word.lower() == key.lower():
                                #print("Match found for",key)
                                myScore = myScore + SearchDict[key]
                row[0] = myScore
                #print("SCORE:",myScore)
                #print("COUNT:",count)
                if count==50000 or count==100000 or count==150000 or count==200000 or count==250000 or count==300000 or count==350000 or count==400000 or count==450000:
                    print("Program still running, count at",count)

                cursor.updateRow(row)
                
                #save the valid articles in html format to a folder
                page = urllib.request.urlopen(URL,timeout=5)
                with open(os.path.join(save_folder,"htmlFile_"+str(count)+".html"),"w") as outFile:
                    outFile.write(page.read().decode('utf-8'))
                #print("Article",count,"written to HTML save folder",save_folder)
            
            except:
                exception = sys.exc_info()[0]
                print("Exception raised:",str(exception),'\n')
                traceback.print_exc()
                pass
            count+=1
        
    print("Finished")


# In[4]:


TableFilepath = 'C:\\Users\\amarti32\\Desktop\\MyFiles\\CBP\\WebScraped.gdb\\'
fields = ["Score","Did"]
SearchTermsFilepath = "C:\\Users\\amarti32\\Desktop\\MyFiles\\CBP\\"
searcDict = "SearchTermDict.xlsx"
save_folder = "C:\\Users\\amarti32\\Desktop\\MyFiles\\CBP\\URL_HTML_FILES"

First500Ktable = Table(TableFilepath,"First500KEvents")
Events500kTo1M = Table(TableFilepath,"Events500Kto1M")
Events1Mto1_5M = Table(TableFilepath,"Events1Mto1_5M")
Events1_5MtoEnd = Table(TableFilepath,"Events1_5MtoEnd")


KeyList, SearchDict = SearchTerms(SearchTermsFilepath,searcDict)


# In[ ]:


URLScrapeNScore(First500Ktable,fields,KeyList,SearchDict,save_folder)

