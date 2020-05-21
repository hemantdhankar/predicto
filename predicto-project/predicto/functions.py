import glob
import time
import os
import glob
from matplotlib import pyplot as plt
import smtplib, os, sys
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from html.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

def run_task(file, name, email, sequence):
	if(sequence):
		make_file(sequence)
	binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
	pwd = os.getcwd()
	pwd=pwd+'\\geckodriver.exe'
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options, firefox_binary=binary,executable_path=pwd)
	master = []
	if(sequence):
		BLAST(driver, master, 'sample.fa')
		send_email(name, email, master, 'sample.fa')
	else:
		BLAST(driver, master, file.name)
		send_email(name, email, master, file.name)


def make_file(sequence):
    with open('static/upload/sample.fa', 'w+') as destination:  
        for chunk in sequence:
            destination.write(chunk)


def handle_uploaded_file(f):  
    with open('static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():
            destination.write(chunk)

def VIZ(organs,final):
    try:
        fig,ax = plt.subplots()
        sep = (0.3,0.3,0.3,0.3,0.3)
        col = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#d22d2d']
        ax.pie(
            final,
            explode = sep,
            labels = organs,
            autopct = '%1.1f%%',
            colors = col,
            shadow = True,
            startangle = 90)
        ax.axis('equal')
        plt.tight_layout()
        plt.savefig('static/output/pred_result.png')
    except :
        print("Oops!", sys.exc_info()[0], "occured.")
        print("Cannot make predictions for this virus...")
        print("Not enough results were generated from the queries!!!")

def PUBMED(microbes, m1p, m2p, m3p, driver):
    
    final = [0]*5
    
    organs = ['heart','kidney','lungs','liver','brain']

    m1p = list(filter(lambda x:x != '',list(dict.fromkeys(m1p))))
    m2p = list(filter(lambda x:x != '',list(dict.fromkeys(m2p))))
    m3p = list(filter(lambda x:x != '',list(dict.fromkeys(m3p))))


    driver.get('https://pubmed.ncbi.nlm.nih.gov/')      # PUBMED
    
    co = 0
    for j in range(len(organs)):
        query =  '('+m1p[0]+' AND '+organs[j]+') OR ('+m1p[1]+' AND '+organs[j]+') OR ('+m1p[2]+' AND '+organs[j]+')'
        #query = i+' AND '+organs[j]
        #query = microbes[0] + ' AND ' + i + ' AND ' + organs[j]
        try:
            driver.find_element_by_xpath('//*[@id="search-form"]/div[1]/div[1]/div/a').click()
        except:
            pass        
        driver.find_element_by_xpath('//*[@id="id_term"]').send_keys(query)
        driver.find_element_by_xpath('//*[@id="search-form"]/div/div[1]/div/button').click()
        try:
            print(co)
            co+=1
            result=driver.find_element_by_xpath('//*[@id="search-results"]/div[2]/div[1]/span').text.split()
            try:
                driver.find_element_by_xpath('/html/body/main/div[9]/div[2]/section/em[2]').text
                print("Not considered")
            except:                
                result[0] = result[0].replace(',','')
                final[j]+=int(result[0])
                print(query, result[0])
        except:
            print("ok")
            pass

    for j in range(len(organs)):
        query = '('+m2p[0]+' AND '+organs[j]+') OR ('+m2p[1]+' AND '+organs[j]+') OR ('+m2p[2]+' AND '+organs[j]+')'
        #query = i+' AND '+organs[j]
        #query = microbes[1] + ' AND ' + i + ' AND ' + organs[j]
        try:
            driver.find_element_by_xpath('//*[@id="search-form"]/div[1]/div[1]/div/a').click()
        except:
            pass

        driver.find_element_by_xpath('//*[@id="id_term"]').send_keys(query)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="search-form"]/div/div[1]/div/button').click()
        try:
            print(co)
            co+=1
            result=driver.find_element_by_xpath('//*[@id="search-results"]/div[2]/div[1]/span').text.split()
            try:
                driver.find_element_by_xpath('/html/body/main/div[9]/div[2]/section/em[2]').text
                print("Not considered")
            except:                
                result[0] = result[0].replace(',','')
                final[j]+=int(result[0])
                print(query, result[0])
        except:
            print("ok")
            pass

    for j in range(len(organs)):
        query = '('+m3p[0]+' AND '+organs[j]+') OR ('+m3p[1]+' AND '+organs[j]+') OR ('+m3p[2]+' AND '+organs[j]+')'
        #query = i+' AND '+organs[j]
        #query = microbes[2] + ' AND ' + i + ' AND ' + organs[j]
        try:
            driver.find_element_by_xpath('//*[@id="search-form"]/div[1]/div[1]/div/a').click()
        except:
            pass

        driver.find_element_by_xpath('//*[@id="id_term"]').send_keys(query)
        driver.find_element_by_xpath('//*[@id="search-form"]/div/div[1]/div/button').click()
        try:
            print(co)
            co+=1
            result=driver.find_element_by_xpath('//*[@id="search-results"]/div[2]/div[1]/span').text.split()
            try:
                driver.find_element_by_xpath('/html/body/main/div[9]/div[2]/section/em[2]').text
                print("Not considered")
            except:                
                result[0] = result[0].replace(',','')
                final[j]+=int(result[0])
                print(query, result[0])
        except:
            print("ok")
            pass
    
    for i in microbes:
        for j in range(len(organs)):
            query = i+' AND '+organs[j]
            #query = microbes[2] + ' AND ' + i + ' AND ' + organs[j]
            try:
                driver.find_element_by_xpath('//*[@id="search-form"]/div[1]/div[1]/div/a').click()
            except:
                pass

            driver.find_element_by_xpath('//*[@id="id_term"]').send_keys(query)
            driver.find_element_by_xpath('//*[@id="search-form"]/div/div[1]/div/button').click()
            try:
                print(co)
                co+=1
                result=driver.find_element_by_xpath('//*[@id="search-results"]/div[2]/div[1]/span').text.split()
                try:
                    driver.find_element_by_xpath('/html/body/main/div[9]/div[2]/section/em[2]').text
                    print("Not considered")
                except:                
                    result[0] = result[0].replace(',','')
                    final[j]+=int(result[0])
                    print(query, result[0])
            except:
                print("ok")
                pass

    print(final)
    VIZ(organs,final)



def PDB(microbes, driver, master):
    m1p=['','','']
    m2p=['','','']
    m3p=['','','']

    driver.get("https://www.rcsb.org/pdb/static.do?p=search/index.html")                        # PDB
    driver.find_element_by_xpath("//*[@id='search-bar-input-text']").send_keys(microbes[0])     # search for 1st microbe
    driver.find_element_by_xpath('//*[@id="search-icon"]').click()
    sleep(15)    
    m1p[0]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[1]/div[2]/table[1]/tr/td[1]/h3/a').text
    m1p[1]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[2]/div[2]/table[1]/tr/td[1]/h3/a').text
    m1p[2]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[3]/div[2]/table[1]/tr/td[1]/h3/a').text
    for i in range(len(m1p)):
        splitted = m1p[i].split(' ')
        m1p[i] = splitted[0]

    print("Top 3 proteins of ",microbes[0],' -> ',m1p)
    master.append(str(microbes[0])+"->"+str(m1p))

    if microbes[1] != '':
        driver.find_element_by_xpath("//*[@id='search-bar-input-text']").clear()
        driver.find_element_by_xpath("//*[@id='search-bar-input-text']").send_keys(microbes[1])
        driver.find_element_by_xpath('//*[@id="search-icon"]').click()
        sleep(15)    
        m2p[0]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[1]/div[2]/table[1]/tr/td[1]/h3/a').text
        m2p[1]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[2]/div[2]/table[1]/tr/td[1]/h3/a').text
        m2p[2]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[3]/div[2]/table[1]/tr/td[1]/h3/a').text
        for i in range(len(m2p)):
            splitted = m2p[i].split(' ')
            m2p[i] = splitted[0]
        print("Top 3 proteins of ",microbes[1],' -> ',m2p)
        master.append(str(microbes[1])+"->"+str(m2p))

    if microbes[2] != '':
        driver.find_element_by_xpath("//*[@id='search-bar-input-text']").clear()
        driver.find_element_by_xpath("//*[@id='search-bar-input-text']").send_keys(microbes[2])
        driver.find_element_by_xpath('//*[@id="search-icon"]').click()
        sleep(15)                                                
        m3p[0]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[1]/div[2]/table[1]/tr/td[1]/h3/a').text
        m3p[1]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[2]/div[2]/table[1]/tr/td[1]/h3/a').text
        m3p[2]=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[4]/div[2]/div[2]/table/tr/td[2]/div/div[3]/div[3]/div[3]/div[2]/table[1]/tr/td[1]/h3/a').text
        for i in range(len(m3p)):
            splitted = m2p[i].split(' ')
            m3p[i] = splitted[0]
        print("Top 3 proteins of ",microbes[2],' -> ',m3p)
        master.append(str(microbes[2])+"->"+str(m3p))

    PUBMED(microbes, m1p, m2p, m3p, driver)

def BLAST(driver, master, filename):
    
    driver.get("https://www.genome.jp/tools/blast/")    # blast webiste
    sleep(2)
    
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/div/table/tbody/tr/td/form/table[2]/tbody/tr[2]/td[2]/input").send_keys(os.getcwd()+"\\static\\upload\\"+filename)
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
    temp0 = res[2].split('|')
    temp1 = res[3].split('|')
    temp2 = res[4].split('|')
    microbes[0] = temp0[0]
    microbes[1] = temp1[0]
    microbes[2] = temp2[0]
    if(microbes[0][-3:]=="..."):
        microbes[0]=microbes[0][:-3]
    if(microbes[1][-3:]=="..."):
        microbes[1]=microbes[0][:-3]
    if(microbes[2][-3:]=="..."):
        microbes[2]=microbes[0][:-3]
    
    print(microbes)

    PDB(microbes, driver, master)


def send_email(name, user_email, master, filename):	
	attachments = glob.glob("static/output/*")
	attachments.extend(glob.glob("static/upload/"+filename))
	print(attachments)
	username = 'predictoserver'
	password = 'predicto@pb'
	host = 'smtp.gmail.com:587' 

	fromaddr = 'predictoserver@gmail.com' 
	toaddr  = user_email
	replyto = fromaddr

	msgsubject = "Your Result from PredictO"

	htmlmsgtext = """<h2>Hi """+name+""",</h2>"""
	htmlmsgtext	= htmlmsgtext+"""<p>We have analysed your sequence files on our PredictO Server and here is your result.<br><br><b>Top Matched Virus -> Top Protiens of that virus</b><br>"""
	for i in master:
		htmlmsgtext = htmlmsgtext + i + """<br>"""
	htmlmsgtext=htmlmsgtext+"""<br>Hope you liked our service. As we are still in devoloping phase feedbacks are highly appreciated.<br>Best of luck!<br></p><h3>Team PredictO</h3><p><strong>Please find the attached piechart representing the chances of an organ to be a potential target.</strong></p><br />"""


	class MLStripper(HTMLParser):
	    def __init__(self):
	        self.reset()
	        self.convert_charrefs=True
	        self.fed = []
	    def handle_data(self, d):
	        self.fed.append(d)
	    def get_data(self):
	        return ''.join(self.fed)

	def strip_tags(html):
	    s = MLStripper()
	    s.feed(html)
	    return s.get_data()

	########################################################################

	try:
	    # Make text version from HTML - First convert tags that produce a line break to carriage returns
	    msgtext = htmlmsgtext.replace('</br>',"\r").replace('<br />',"\r").replace('</p>',"\r")
	    # Then strip all the other tags out
	    msgtext = strip_tags(msgtext)

	    # necessary mimey stuff
	    msg = MIMEMultipart()
	    msg.preamble = 'This is a multi-part message in MIME format.\n'
	    msg.epilogue = ''

	    body = MIMEMultipart('alternative')
	    body.attach(MIMEText(msgtext))
	    body.attach(MIMEText(htmlmsgtext, 'html'))
	    msg.attach(body)
	    #print('attachments' in globals())
	    if len(attachments) > 0: # are there attachments?
	        for filename in attachments:
	            f = filename
	            print(f)
	            part = MIMEBase('application', "octet-stream")
	            part.set_payload( open(f,"rb").read() )
	            encoders.encode_base64(part)
	            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
	            msg.attach(part)

	    msg.add_header('From', fromaddr)
	    msg.add_header('To', toaddr)
	    msg.add_header('Subject', msgsubject)
	    msg.add_header('Reply-To', replyto)

	    # The actual email sendy bits
	    server = smtplib.SMTP(host)
	    server.set_debuglevel(False) # set to True for verbose output
	    try:
	        # gmail expect tls
	        server.starttls()
	        server.login(username,password)
	        server.sendmail(msg['From'], [msg['To']], msg.as_string())
	        print('Email sent')
	        server.quit() # bye bye
	    except:
	        # if tls is set for non-tls servers you would have raised an exception, so....
	        server.login(username,password)
	        server.sendmail(msg['From'], [msg['To']], msg.as_string())
	        print('Email sent')
	        server.quit() # sbye bye        
	except:
	    print ('Email NOT sent to %s successfully. %s ERR: %s %s %s ', str(toaddr), 'tete', str(sys.exc_info()[0]), str(sys.exc_info()[1]), str(sys.exc_info()[2]) )
	    #just in case
