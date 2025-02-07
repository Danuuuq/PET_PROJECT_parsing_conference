import subprocess
import smtplib
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_mail = 'conference@invest.gazprom.ru'
# to_mail = ('epetukhova@invest.gazprom.ru', 'vvmarchenko@invest.gazprom.ru', 'dtyunkov@invest.gazprom.ru')
to_mail =  'dtyunkov@invest.gazprom.ru'
server_email = 'mail.vk.giz.int'


def format_attach(data):
    return f'Новые совещания в расписании: {data}'


def send_email(data):
    current_day = datetime.now().strftime('%Y-%m-%d %H:%M')
    subject = f'Совещания на {current_day}'
    msg = MIMEMultipart()
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(format_attach(data), 'html', 'utf-8'))
    smtp = smtplib.SMTP(server_email)
    smtp.sendmail(from_mail, to_mail, msg.as_string())
    smtp.quit()


def scp_send_csv(file):
    host = '10.7.84.238'
    user = 'support'
    password = 'Rhfcysq,tutvjn+50%'
    remote_dir = '/home/support/conference'
    scp_command = [
        'sshpass', '-p', password,
        'scp', file, f'{user}@{host}:{remote_dir}'
    ]
    try:
        result = subprocess.run(scp_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('Файл успешно отправлен')
    except subprocess.CalledProcessError as e:
        print('Не отправился файл')
