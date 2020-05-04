import smtplib
import datetime
from email.mime.multipart import MIMEMultipart


class Gmail:
    def __init__(self):
        return

    def send_email(self, body):
        """
        Takes 1 argument body[body of email built from Builder
        class in template_builder.py that uses email.html]
        -> returns nothing
        """
        try:
            # gmail authentication 
            gmail_user = 'cooperwakefield@gmail.com'
            gmail_password = 'otlkxnfszbfauqhb'

            # set email configuration
            msg = MIMEMultipart('alternative')
            msg.attach(body)
            msg['From'] = gmail_user
            msg['To'] = 'enquiries@cooperwakefield.com'
            now = datetime.datetime.now()
            msg['Subject'] = str(now.month) + '-' + str(now.day) + '-' + str(now.year) + 'Stock Insights'

            # send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.close()
        except Exception as e:
            print(str(e))
