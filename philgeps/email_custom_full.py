import smtplib, zipfile, os, datetime
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import subprocess
import pandas as pd

csv_output_file_old = r"csv_output/data_full_data.csv"
c_date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_output_file = r"csv_output/data_full_data_" + str(c_date_time) + ".xlsx"

read_file = pd.read_csv (csv_output_file_old)
read_file.to_excel (csv_output_file, index = None, header=True)

#os.rename(csv_output_file_old, csv_output_file)

def email_send_gmail():
        
        fromaddr = "XXXXX@gmail.com"
        toaddr = "XXXX@gmail.com"
        pwd = '*******'
        c_date = datetime.datetime.now().strftime("%d-%b-%Y %I-%M %p")
        subject_line = "PhilGEPS - Open Opportunities | " + str(c_date)
        body = "Please find attached automated report"
        filename = csv_output_file

        # instance of MIMEMultipart 
        msg = MIMEMultipart() 

        msg['From'] = fromaddr 
        msg['To'] = toaddr 
        msg['Subject'] = subject_line
        msg.attach(MIMEText(body, 'plain')) 
        attachment = open(filename, "rb") 

        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
        p.set_payload((attachment).read()) 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        msg.attach(p) 

        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 

        # start TLS for security and Authentication 
        s.starttls()
        s.login(fromaddr, pwd) 

        # Converts the Multipart msg into a string 
        text = msg.as_string() 

        # sending the mail and terminating the session 
        s.sendmail(fromaddr, toaddr, text) 

        s.quit()
        print("Email Sent Successfully")


def email_linux():
        #CMD = 'echo "Philgeps report" | mail -s "PHILGEPS DAILY REPORT" -a %s info@opellconstruction.com opellconstruction@gmail.com' % csv_output_file
        CMD = 'echo "Philgeps report" | mail -s "PHILGEPS DAILY REPORT" -a %s txtmate@gmail.com opellconstruction@gmail.com' % csv_output_file
        #CMD = 'echo "Philgeps report" | mail -s "PHILGEPS DAILY REPORT" -a %s priyanka.butle2000@gmail.com' % csv_output_file
        ps = subprocess.Popen(CMD,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print("Email Sent Successfully")

#email_send_gmail()
email_linux()