from email.mime.base import MIMEBase
import smtplib
from smtplib import SMTPDataError
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from database_handler import Helpers
from database_handler import config as CONFIG
from os import path


class SendMail:
    @staticmethod
    def send_email(email_message: str, subject: str, email_recepients: list, file_attachments=[], attempt=0, email_server='secondary_server'):
        print(email_server)
        print(email_server)
        if attempt == 0:
            try:
                config = CONFIG('.config.ini', 'email_server')
                params = config.read_config()
            except Exception as ex:
                raise ex
        elif attempt < 5 and attempt > 0:
            if email_server is None:
                raise Exception("No Secondary Email Server Name provided")
            else:
                try:
                    config = CONFIG('.config.ini', email_server)
                    params = config.read_config()
                except Exception as ex:
                    raise ex
                
        else:
            raise Exception("Emailing attempt stopped at 5 tries")

     

        try:
            port = params['port']
            smtp_server = params['smtp_server']
            sender_email = params['sender_email']
            #sender_username = params['sender_username']
            login_email = params['sender_username']
            password = params['password']
            platform = params['platform']
            Bcc = ''

            message = MIMEMultipart()
            message['Subject'] = '%s' % (subject)
            message['From'] = sender_email
            message['To'] = ", ".join(email_recepients)
            message['Cc'] = None

            html = '''
            <html>
            <head></head>
            <body>
            <p>Hello Team.
            <br> 
            %s 
            </p>
            </body>
            </html>
            ''' %(email_message)

            message.attach(MIMEText(html, 'html'))
            if file_attachments is not None or len(file_attachments) > 0:
                for filename in file_attachments:
                    if path.isdir(path.split(filename)[0]):
                        filenamex = path.split(filename)[-1]
                    else:
                        filenamex = filename
                    with open(filename, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)

                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={filenamex}',
                    )

                    message.attach(part)

            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                print('sending mail started.....')
                server.starttls(context=context)
                server.login(login_email, password)
                server.sendmail(sender_email, email_recepients, message.as_string())
                print('sending mail ended.....')
        
        except SMTPDataError as e:
            if attempt == 0:
                print(f"SMTPDataError occurred, retrying with attempt = 1")
                SendMail.send_email(email_message, subject, email_recepients, file_attachments, attempt=1, email_server=email_server)
            else:
                error_code, error_message = e.smtp_code, e.smtp_error
                print(f"SMTPDataError: ({error_code}, {error_message})")

        except Exception as ex:
            raise ex
        
        return 'Email should be sent successfully.'