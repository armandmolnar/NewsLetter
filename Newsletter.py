import MySQLdb.connections
import os
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

"""
pathlib might be used instead of os:  from pathlib import Path
https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module

os.path.exists() => Path.exists()
os.listdir() => Path.iterdir()
os.path.isdir() => Path.is_dir()
os.path.splitext() => PurePath.suffix
"""
mydb = MySQLdb.connections.Connection(
    host="localhost",
    user="newsletter_user",
    password="demo123",
    database="django_auth"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT customerID,email FROM core_user")
# todo database connect error should be handled: print(mydb.show_warnings())
# todo select first_name,last_name is kell
# todo emailtörzsbe megszólítás {first_name}+{last_name} is kell


myresult = dict(mycursor.fetchall())

newsletter_folder = r"C:/newsletter/napi"
assert os.path.exists(newsletter_folder), "This folder does not exist!"
assert os.path.isdir(newsletter_folder), "Path must be a folder."
allowed_extensions = [".xlsx"]
folder_content = os.listdir(newsletter_folder)

emails_files = {}
for file in folder_content:
    name, ext = os.path.splitext(file)
    if ext.lower() in allowed_extensions:
        if myresult.get(name[:6]):
#            file_full_path = os.path.join(newsletter_folder, file)
            emails_files[myresult[name[:6]]] = file
# ha nem file_full_path -ot hasznalunk es nem a newsletter.py dir-jében van a kuldendo excel akkor directory change kell:

os.chdir(newsletter_folder)

for key in emails_files:
    msg = EmailMessage()
    msg['Subject'] = 'Most már van Content-Type: text/plain'
    msg['From'] = 'proba@ibm.hu'
    msg['To'] = key
    msg.set_content("""\
    Tisztelt !
    Üdvözlettel, 
    proba@ibm.hu
    """)
    with open(emails_files[key], 'rb') as f:
        xlsx = f.read()
        msg.add_attachment(xlsx, maintype="application", subtype="xlsx", filename=emails_files[key])
    s = smtplib.SMTP('localhost)
    s.send_message(msg)
    s.quit()
