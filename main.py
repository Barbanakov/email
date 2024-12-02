from tkinter import *
import smtplib
from email.message import EmailMessage


def send_email():
    # sender_email = 'barbanakov.sergey@yandex.ru'
    # recipient_email = 'nikomu@mail.ru'
    # password = 'afmdurglqtrivmqy'
    # subject = 'Проверка связи 1'
    # body = 'Привет 1 из python'
    sender_email = sender_email_entry.get()
    recipient_email = recipient_email_entry.get()
    password = password_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", END)

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # server = None

    try:
        # использование порта 465 для SSL
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(sender_email, password)
        server.send_message(msg)
        # print('Письмо отправлено!')
        result_label.config(text='Письмо отправлено!')
    except Exception as e:
        # print(f'Ошибка {e}')
        result_label.config(text=f'Ошибка: {e}')
    finally:
        if server:
            server.quit()


# Создание главного окна
window = Tk()
window.title("Отправка Email")
window.geometry("500x300")
# Создание и размещение виджетов
Label(text="Отправитель (Email):").grid(row=0, column=0, sticky=W)
sender_email_entry = Entry(window)
sender_email_entry.grid(row=0, column=1)

Label(text="Получатель (Email):").grid(row=1, column=0, sticky=W)
recipient_email_entry = Entry(window)
recipient_email_entry.grid(row=1, column=1)

Label(text="Пароль приложения:").grid(row=2, column=0, sticky=W)
password_entry = Entry(show="*")
password_entry.grid(row=2, column=1)

Label(text="Тема:").grid(row=3, column=0, sticky=W)
subject_entry = Entry(window)
subject_entry.grid(row=3, column=1)

Label(text="Сообщение:").grid(row=4, column=0, sticky=N)
body_text = Text(height=10, width=45) # многострочное текстовое поле
body_text.grid(row=4, column=1)

Button(text="Отправить", command=send_email).grid(row=5, column=1, sticky=E)

result_label = Label(text="")
result_label.grid(row=6, column=1, sticky=W)

# Запуск главного цикла окна
window.mainloop()
