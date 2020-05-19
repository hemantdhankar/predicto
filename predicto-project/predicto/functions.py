import glob
import time
import os
import glob
import plotly.graph_objects as go
import smtplib, os, sys
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from html.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

def run_task(file, name, email):
	with open(str(file.name), 'r') as f:
	    seq = f.read().replace('\n', '')

	binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
	pwd = os.getcwd()
	pwd=pwd+'\\geckodriver.exe'
	driver = webdriver.Firefox(firefox_binary=binary,executable_path=pwd)
	BLAST(seq)


def handle_uploaded_file(f):  
    with open('static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():
            destination.write(chunk)

def VIZ(organs,final):

    total = sum(final)
    
    for i in range(len(final)):
        final[i] = round((final[i]/total)*100,1)

    fig = go.Figure(data=[go.Bar(
        x = organs, y=final,
        text=final,
        textposition='auto',
    )])

    fig.update_layout(
    width =500,
    height=500,
    )

    fig.show()

def PUBMED(microbes, m1p, m2p, m3p):
    
    final = [0]*4
    
    organs = ['heart','kidney','lungs','liver']

    m1p = list(filter(lambda x:x != '',list(dict.fromkeys(m1p))))
    m2p = list(filter(lambda x:x != '',list(dict.fromkeys(m2p))))
    m3p = list(filter(lambda x:x != '',list(dict.fromkeys(m3p))))


    driver.get('https://www.ncbi.nlm.nih.gov/pubmed/')      # PUBMED
    
    co = 0
    for i in m1p:
        for j in range(len(organs)):
            query = microbes[0] + ' AND ' + i + ' AND ' + organs[j]
            driver.find_element_by_xpath('//*[@id="term"]').clear()
            driver.find_element_by_xpath('//*[@id="term"]').send_keys(query)
            driver.find_element_by_xpath('//*[@id="search"]').click()
            try:
                print(co)
                co+=1
                result=driver.find_element_by_xpath('/html/body/div[2]/div[1]/form/div[1]/div[7]/div/div[3]/div[1]/h3').text.split()
                final[j]+=int(result[-1])
                print(query, result[-1])
            except:
                print("ok")
                pass

    for i in m2p:
        for j in range(len(organs)):
            query = microbes[1] + ' AND ' + i + ' AND ' + organs[j]
            driver.find_element_by_xpath('//*[@id="term"]').clear()
            driver.find_element_by_xpath('//*[@id="term"]').send_keys(query)
            driver.find_element_by_xpath('//*[@id="search"]').click()
            try:
                print(co)
                co+=1
                result=driver.find_element_by_xpath('/html/body/div[2]/div[1]/form/div[1]/div[7]/div/div[3]/div[1]/h3').text.split()
                final[j]+=int(result[-1])    
                print(query, result[-1])
            except:
                print("ok")
                pass

    for i in m3p:
        for j in range(len(organs)):
            query = microbes[2] + ' AND ' + i + ' AND ' + organs[j]
            driver.find_element_by_xpath('//*[@id="term"]').clear()
            driver.find_element_by_xpath('//*[@id="term"]').send_keys(query)
            driver.find_element_by_xpath('//*[@id="search"]').click()
            try:
                print(co)
                co+=1
                result=driver.find_element_by_xpath('/html/body/div[2]/div[1]/form/div[1]/div[7]/div/div[3]/div[1]/h3').text.split()
                final[j]+=int(result[-1])
                print(query, result[-1])
            except:
                print("ok")
                pass

    print(final)
    VIZ(organs,final)



def PDB(microbes):
    m1p=['','','']
    m2p=['','','']
    m3p=['','','']

    driver.get("https://www.rcsb.org/pdb/static.do?p=search/index.html")                        # PDB
    driver.find_element_by_xpath("//*[@id='search-bar-input-text']").send_keys(microbes[0])     # search for 1st microbe
    driver.find_element_by_xpath('//*[@id="search-icon"]').click()
    sleep(15)    
    m1p[0]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[1]/div[2]/table[2]/tbody/tr[2]/td[2]/div/a').text
    m1p[1]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[2]/div[2]/table[2]/tbody/tr[2]/td[2]/div/a').text
    m1p[2]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[3]/div[2]/table[2]/tbody/tr[2]/td[2]/div/a').text
    for i in range(len(m1p)):
        splitted = m1p[i].split(' ')
        m1p[i] = splitted[0]

    print("Top 3 proteins of ",microbes[0],' -> ',m1p)

    if microbes[1] != '':
        driver.find_element_by_xpath("//*[@id='search-bar-input-text']").clear()
        driver.find_element_by_xpath("//*[@id='search-bar-input-text']").send_keys(microbes[1])
        driver.find_element_by_xpath('//*[@id="search-icon"]').click()
        sleep(15)    
        m2p[0]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[1]/div[2]/table[2]/tbody/tr[2]/td[2]/div/a').text
        m2p[1]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[2]/div[2]/table[2]/tbody/tr[2]/td[2]/div/a').text
        m2p[2]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[3]/div[2]/table[2]/tbody/tr[2]/td[2]/div/a').text
        for i in range(len(m2p)):
            splitted = m2p[i].split(' ')
            m2p[i] = splitted[0]
        print("Top 3 proteins of ",microbes[1],' -> ',m2p)

    if microbes[2] != '':
        driver.find_element_by_xpath("//*[@id='search-bar-input-text']").clear()
        driver.find_element_by_xpath("//*[@id='search-bar-input-text']").send_keys(microbes[2])
        driver.find_element_by_xpath('//*[@id="search-icon"]').click()
        sleep(15)                                                
        m3p[0]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[1]/div[2]/table[2]/tbody/tr[2]/td[2]/div/a').text
        m3p[1]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[2]/div[2]/table[2]/tbody/tr[2]/td[2]/div/a').text
        m3p[2]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[3]/div[2]/table[2]/tbody/tr[2]/td[2]/div/a').text
        for i in range(len(m3p)):
            splitted = m2p[i].split(' ')
            m3p[i] = splitted[0]
        print("Top 3 proteins of ",microbes[2],' -> ',m3p)

    PUBMED(microbes, m1p, m2p, m3p)

def BLAST(seq):
    
    driver.get("https://www.genome.jp/tools/blast/")    # blast webiste
    sleep(2)
    
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/div/table/tbody/tr/td/form/table[2]/tbody/tr[3]/td[2]/textarea").click()
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/div/table/tbody/tr/td/form/table[2]/tbody/tr[3]/td[2]/textarea").send_keys(seq)       # fill the seq  
    driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/div/table/tbody/tr/td/form/table[3]/tbody/tr[2]/td[1]/input[1]').click()               # select BlastN
    driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/div/table/tbody/tr/td/form/table[3]/tbody/tr[2]/td[2]/table/tbody/tr/td/input[19]').click()    # select Virus DB
    driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/div/table/tbody/tr/td/form/table[1]/tbody/tr/td/input[1]').click()           # search
    sleep(10)

    microbes=['','','']

    x=driver.find_element_by_xpath('/html/body/form/pre').text
    y=x.split('  ')
    res=[]
    for i in y:
        if len(i) > 40:
            res.append(i)
    
    temp0 = res[2].split()
    temp1 = res[3].split()
    temp2 = res[4].split()
    microbes[0] = temp0[0]+' '+temp0[1]
    microbes[1] = temp1[0]+' '+temp1[1]
    microbes[2] = temp2[0]+' '+temp2[1]
    
    print(microbes)

    PDB(microbes)

