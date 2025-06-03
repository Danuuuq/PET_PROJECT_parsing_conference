import subprocess
import smtplib
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_mail = 'SECRET_DATA'
to_mail = 'SECRET_DATA'
server_email = 'SECRET_DATA'


def format_attach(current_time, new_conf, today_conf):
    message = """
    <html>
     <head></head>
      <body>
        <h2>Новые совещания после: {current_time}</h2>
          <table>
            <tr>
              <td>Время начала</td>
              <td>|Время окончания</td>
              <td>|Студии</td>
              <td>|Комментарий</td>
              <td>|Организатор</td>
              <td>|Ответственный</td>
            </tr>
    """.format(current_time=current_time)
    for conf in new_conf:
        message += """<td>{start}</td>
                    <td>|{end}</td>
                    <td>|{room}</td>
                    <td>|{comment}</td>
                    <td>|{org}</td>
                    <td>|{man}</td></tr>""".format(
                        # date=conf['date'],
                        start=conf['start_time'],
                        end=conf['end_time'],
                        room=', '.join(conf['room']),
                        comment=conf['comment'],
                        org=conf['organizer'],
                        man=conf['manager']
                    )
    message += "</table>"
    if len(today_conf.all()) != 0:
        message += """
            <br><br><br>
            <h2>Все совещания на сегодня</h2>
              <table>
                <tr>
                  <td>Время начала</td>
                  <td>|Время окончания</td>
                  <td>|Студии</td>
                  <td>|Комментарий</td>
                  <td>|Организатор</td>
                  <td>|Ответственный</td>
                </tr>
        """
        for conf in today_conf:
            conf = conf.__dict__
            message += """<td>{start}</td>
                        <td>|{end}</td>
                        <td>|{room}</td>
                        <td>|{comment}</td>
                        <td>|{org}</td>
                        <td>|{man}</td></tr>""".format(
                            # date=conf['date'],
                            start=conf['start'].strftime('%H:%M'),
                            end=conf['end'].strftime('%H:%M'),
                            room=conf['rooms'],
                            comment=conf['comment'],
                            org=conf['organizer'],
                            man=conf['manager']
                        )
    message += "</table>"
    message += """
     </body>
    </html>
    """
    return message


def send_email(new_conf, today_conf):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    subject = f'Новые совещания на {current_time}'
    msg = MIMEMultipart()
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(format_attach(current_time, new_conf, today_conf), 'html', 'utf-8'))
    smtp = smtplib.SMTP(server_email)
    smtp.sendmail(from_mail, to_mail.split(','), msg.as_string())
    smtp.quit()
