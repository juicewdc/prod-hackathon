import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from admin_settings import notifications_password
from admin_settings import notifications_login


theme = input("Введите тему уведомления: ")
text = input("Введите текст уведомления: ")

notif_login = notifications_login
notif_pwd = notifications_password
user_id = "mikuakidera@gmail.com"

def send_notification(notif_login, notif_pwd, user_id, text, theme):

    message = MIMEMultipart()
    message['From'] = notif_login
    message['To'] = user_id
    message['Subject'] = theme
    message.attach(MIMEText(text, 'plain'))

    try:
        smtp_server = smtplib.SMTP('smtp.yandex.ru', 587)
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(notif_login, notif_pwd)
        smtp_server.sendmail(notif_login, user_id, message.as_string())
        print("Сообщение успешно отправлено!")
        smtp_server.quit()
    except Exception as err:
        print('Произошла какая-то ошибка!')
        print(err)

send_notification(notif_login, notif_pwd, user_id, text, theme)
