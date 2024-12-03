from tkinter import *
import smtplib
from email.message import EmailMessage
from email.utils import parseaddr


def validate_email(email):
    # Проверка email на соответствие стандартному формату.
    name, addr = parseaddr(email) # парсинг email и в переменные name и addr записывается из эл. письма имя и адрес
    return '@' in addr and '.' in addr.split('@')[-1] # возвращается True если есть "@" в адресе, а также есть "."
                                                # в последней части адреса, разрезанного по символу "@" (индекс [-1])


def save():
    with open("save.txt", "w") as file: # открывается файл для записи, если его нет, то создаётся
        file.write(sender_email_entry.get() + '\n')
        file.write(recipient_email_entry.get() + '\n')
        file.write(password_entry.get() + '\n')


def load():
    try:
        with open("save.txt", "r") as file: # открывается файл для чтения (и потом автоматически закрывается)
            credentials = file.readlines()
            sender_email_entry.insert(0, credentials[0].strip()) # поле заполняется из файла, строка с индексом 0
                                                                        # (.strip удаляет всё лишнее из строки)
            recipient_email_entry.insert(0, credentials[1].strip()) # поле заполняется из строки с индексом 1
            password_entry.insert(0, credentials[2].strip()) # поле заполняется из строки с индексом 2
    except FileNotFoundError:
        # Файл не найден, игнорируем ошибку:
        pass


def send_email():
    save()
    sender_email = sender_email_entry.get()
    recipient_email = recipient_email_entry.get()

    # Проверка email-адресов, если в любом адресе ошибка, то выход из функции и ничего не отправляется
    if not validate_email(sender_email) or not validate_email(recipient_email):
        result_label.config(text='Ошибка: Неверный формат email')
        return

    password = password_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", END)

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    server = None

    try:
        # использование порта 465 для SSL
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(sender_email, password)
        server.send_message(msg)
        result_label.config(text='Письмо отправлено!')
    except Exception as e:
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

# Загрузка сохраненных данных
load()

# Запуск главного цикла
window.mainloop()
