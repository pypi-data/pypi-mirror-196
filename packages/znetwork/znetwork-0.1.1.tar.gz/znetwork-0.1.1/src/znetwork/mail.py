import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart 
from email.header import Header
from email.utils import formataddr
import os


SENDER_ACCOUNT='398484626@qq.com'   
SENDER_PASSCODE = 'bdweyzlveqrfbgff'             
RECEIVER_ACCOUNT = 'heinz97@aliyun.com'    


class Draft:
    def __init__(self):
        msg = MIMEMultipart() 
        sender_name = 'thinkpad' if t.os_type()=='Windows' else 'ecs'
        receiver_name = 'sx'
        msg['From']=formataddr([sender_name,SENDER_ACCOUNT])  
        msg['To']=formataddr([receiver_name,RECEIVER_ACCOUNT])  
        self.msg = msg

    def write(self, subject, content):       
        self.msg['Subject'] = Header(subject, 'utf-8') 
        self.msg.attach(MIMEText(content, 'plain', 'utf-8'))
        return self

    def add_file(self, path):
        file = open(path, 'rb').read()
        filename = os.path.split(path)[1]
        att = MIMEText(file, 'base64', 'utf-8') 
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s"' % filename
        self.msg.attach(att)
        return self

        
    def send(self):
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  
        server.login(SENDER_ACCOUNT, SENDER_PASSCODE)  
        server.sendmail(SENDER_ACCOUNT,[RECEIVER_ACCOUNT],self.msg.as_string()) 
        server.quit()

def send_text(title,content):
    Draft().write(title,content).send()

    