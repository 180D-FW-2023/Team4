import smtplib
from email.mime.text import MIMEText
import ssl
import ast

# create a secure SSL context
context = ssl.create_default_context()


with open('gui_txt_files/gps.txt', 'r') as f:
    coords = ast.literal_eval(f.read())
f.close()
lat = coords["best_lat"]
lon = coords["best_lon"]

subject = "Fall Detected"
body = "A fall has been detected at https://www.google.com/maps/search/?api=1&query=" +str(lat) + "," + str(lon)
sender = "memorymate.fall.detector@gmail.com"
# recipients = ["jolin51502@gmail.com"]
recipients = []
with open('gui_txt_files/email.txt', 'r') as file:
    # Read all the lines of the file into a list
    recipients = file.readlines()
password = "jmmo dwyv mdoj kass"


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

file = open("gui_txt_files/fall.txt", "r")
content = file.readline()
if content == 'fall\n':
    send_email(subject, body, sender, recipients, password)
elif content =="ADL\n":
    print("Not fall")
# rkbq epqd bkqz yzqv
file.close()
