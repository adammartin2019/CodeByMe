#Load the relevant python libraries
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import pandas as pd
import PyPDF2 as pdf
import docx as dx
import textract as tx

import os
import re


"""

First need to recursively sort through all folders and files in the intern applications folder

R:\Internship Program\Historic Intern Documents\Historic Intern Paperwork and Applications\Intern Applications

Save files to one of three arrays either pdf, doc or docx

once files are saved into the arrays use pool and map to scrape the files for keywords

"""




def FileParser(path):
    
    PDFS = list()
    DOCX = list()
    DOC = list()
    
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith((".pdf")):
                PDFS.append(os.path.join(root,name))
            elif name.endswith((".docx")):
                DOCX.append(os.path.join(root,name))
            elif name.endswith(("resume.doc")):
                DOC.append(os.path.join(root,name))
                
    return {"PDFS":PDFS, "DOCX":DOCX, "DOC":DOC}


def PDFSearch(pdfFile):
    'define search terms'
    
    searchTerms = ['ROTC', 'rotc', 'Reserve Officers Training Corps', 'reserve officer training corps', 'Air Force', 'Army',
                   'Navy', 'Marine','Marines']
        
    try:
        'load file into pdf object'
        PDFobject = pdf.PdfFileReader(pdfFile)
        
        'get number of pages'
        NumPages = PDFobject.getNumPages()
        
        'search each page for keywords'
        for i in range(0,NumPages):
            PageObj = PDFobject.getPage(i)

            TEXT = PageObj.extractText()
        
            "returns a NoneType object if no search word found"
            for j in searchTerms:
                Search = re.search(j,TEXT)
                if Search != None:
                    with open("C:\\Users\\amarti32\\Desktop\\PDFSearch.txt",'a') as text_file:
                        text_file.write("{0} : {1}\n".format(pdfFile, j))
                    break
            else:
                continue
            break
        
    except Exception:
        print("Encountered Error, skipped file", pdfFile)
        with open("C:\\Users\\amarti32\\Desktop\\SkippedFiles.txt",'a') as textfile:
            textfile.write("{0}\n".format(pdfFile))
        pass
            
            


def GetDocxText(file):
    doc = dx.Document(file) 
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


                
def DOCXSearch(docFile):
    'define search terms'
    searchTerms = ['ROTC', 'rotc', 'Reserve Officers Training Corps', 'reserve officer training corps', 'Air Force', 'Army',
                   'Navy', 'Marine','Marines']

    try:
        "Open the file and get the full text"
        TEXT = GetDocxText(docFile)
        
        for i in searchTerms:
            Search = re.search(i,TEXT)
            if Search != None:
                with open("C:\\Users\\amarti32\\Desktop\\DOCXSearch.txt",'a') as textfile:
                    textfile.write("{0} : {1}\n".format(docFile, i))
                break
            else:
                continue
            
    except Exception:
        print("Encountered Error, skipped file", docFile)
        with open("C:\\Users\\amarti32\\Desktop\\SkippedFiles.txt",'a') as textfile:
            textfile.write("{0}\n".format(docFile))
        pass
    
    
    
def DOCSearch(doc):
    'define search terms'
    searchTerms = ['ROTC', 'rotc', 'Reserve Officers Training Corps', 'reserve officer training corps', 'Air Force', 'Army',
                   'Navy', 'Marine','Marines']

    try:
        "Open the file and get the full text"
        TEXT = GetDocxText(doc)
        
        for i in searchTerms:
            Search = re.search(i,TEXT)
            if Search != None:
                with open("C:\\Users\\amarti32\\Desktop\\DocSearch.txt",'a') as textfile:
                    textfile.write("{0} : {1}\n".format(doc, i))
                break
            else:
                continue
    except Exception:
        print("Encountered Error, skipped file", doc)
        with open("C:\\Users\\amarti32\\Desktop\\DocSearch.txt",'a') as textfile:
            textfile.write("{0}\n".format(doc))
        pass
    



   


if __name__ == '__main__':
    
    path = "R:\\Internship Program\\Historic Intern Documents\\Historic Intern Paperwork and Applications\\Intern Applications"
    
    FILES = FileParser(path)
    
    PDFS = FILES['PDFS']
    DOCX = FILES['DOCX']
    DOC = FILES['DOC']
    
    "Allocate the workers"
    pool = Pool()
    print("Beginning scraping of files...\n")
    print("Scraping PDFs")
    pool.map(PDFSearch, PDFS)
    
    print("Scraping DOCXs")
    pool.map(DOCXSearch, DOCX)
    

    pool.close()
    print("No more work submitted to pool instance")
    pool.join()
    
    print("Finished scraping all files")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
          