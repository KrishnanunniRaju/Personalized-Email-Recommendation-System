import time
from email.message import EmailMessage
import smtplib
import os
import random
from dotenv import load_dotenv
from quote import quote
import schedule
from urllib.request import urlopen as uReq
from urllib.request import Request
import ssl
import certifi
from bs4 import BeautifulSoup as bs
import requests

os.chdir("D:\College Material\Sem2\DMML2\ENFUSE\Code\Email_generation")

load_dotenv("login.env")


def send_email(subject, body):
    print("Sending Email...")
    i = random.randint(0, 3)
    sender_tag = "GMAIL_USER" + str(i)
    pass_tag = "GMAIL_PASSWORD" + str(i)
    SENDER = os.environ.get(sender_tag)
    PASSWORD = os.environ.get(pass_tag)

    main_recipient = "dmml2test@gmail.com"
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SENDER
    if random.getrandbits(1):
        msg["To"] = main_recipient
        j = 5
    else:
        msg["CC"] = main_recipient
        j = random.choice([a for a in range(0, 3) if a != i])
        msg["To"] = os.environ.get("GMAIL_USER" + str(j))
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    print(f"Mail Sent from {i} as j={j}")
    server.quit()


#send_email()

def mail_content():
    #scraping template from internet
    print("Getting Content...")
    hdr = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://blog.appsumo.com/business-email-examples/'
    req = Request(url,headers=hdr)
    page = uReq(req, context=ssl.create_default_context(cafile=certifi.where()))
    soup = bs(page)
    template = soup.find_all( "div" , class_='appsumo-textbox' )
    temp_no = random.choice([k for k in range(0,21)])
    
    #creating email template
    print("Creating Template...")
    subject = template[temp_no].find('p').getText()
    body_temp = template[temp_no].find_all('p')
    body = ''
    for i in range(2,len(body_temp)):
        body_text = body_temp[i].getText()
        body = body + '\n' + body_text
    print(body)
    
    #Sending Email
    send_email(subject,body)

mail_content()



    
####Scheduler code####    
#schedule.every(60).seconds.do(send_email)

#while 1:
#    print("Initializing...")
#    schedule.run_pending()
#    time.sleep(5)
