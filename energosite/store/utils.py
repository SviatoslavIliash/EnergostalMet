import requests

from django.core import mail
from django.core.mail import EmailMultiAlternatives

from django.conf import settings


@staticmethod
def send_telegram(order, order_items):
    message = telegram_message(order, order_items)

    TOKEN = ""
    chatId_list = []
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    for chatId in chatId_list:
        try:
            response = requests.post(url, json={'chat_id': chatId, 'text': message, 'parse_mode': 'HTML'})
            print(response.text)
        except Exception as e:
            print(e)

@staticmethod
def telegram_message(order, order_items):
    message = f"<b>Замовлення № {order.pk}</b>\n"
    message += f"Клієнт: {order.user.first_name} {order.user.last_name}\n"
    message += f"Email: {order.user.email}\n"
    message += f"Телефон: {order.user.phone_number}\n"
    message += f"Метод доставки: {order.delivery_method}\n"
    message += f"Місто: {order.city}\n"
    message += f"Відділення/адреса: {order.post_department}\n"
    message += f"Метод оплати: {order.payment_method}\n"
    if order.comment:
        message += f"Коментар: {order.comment}\n"
    message += f"\n<b>Сума замовлення</b>: {order.order_sum}\n"
    if order.order_discount != 0:
        message += f"<b>Сума замовлення зі знижкою</b>: {order.order_sum_w_discount}\n"
    message += "\n<b>Товари:</b>\n"
    for item in order_items:
        message += f"\nНазва: {item.product}\n"
        message += f"Пакування: {item.packaging}\n"
        message += f"Ціна за одиницю: {item.price}\n"
        message += f"Кількість: {item.quantity}\n"
        message += f"Ціна: {item.get_total_price()}\n"

    return message


@staticmethod
def send_email(order, order_items):
    connection = mail.get_connection()  # Use default email connection

    subject = "Ваше замовлення в інтернет-магазині Енергосталь-мет"
    email_from = settings.EMAIL_HOST_USER
    recipients = []
    html_content = email_message(order, order_items)

    messages = []  # email messages to be sent
    for recipient in recipients:
        msg = EmailMultiAlternatives(subject, "", email_from, [recipient])
        msg.attach_alternative(html_content, "text/html")
        messages.append(msg)

    connection.send_messages(messages)


@staticmethod
def email_message(order, order_items):
    message = f"<h3>Дякуємо за замовлення!</h3>" \
              f"<hr>" \
              f"<b>Товари в замовленні № {order.pk}</b><br>" \
              f"<table style=\"border:1px solid #dddddd; border-collapse: collapse; width: 100%;\">" \
              f"<tr>" \
              f"<th style=\"border:1px solid #dddddd;\">Назва</th>" \
              f"<th style=\"border:1px solid #dddddd;\">Пакування</th>" \
              f"<th style=\"border:1px solid #dddddd;\">Ціна за одиницю</th>" \
              f"<th style=\"border:1px solid #dddddd;\">Кількість</th>" \
              f"<th style=\"border:1px solid #dddddd;\">Ціна</th>" \
              f"</tr>"

    for item in order_items:
        message += f"<tr style=\"text-align: left;\">" \
                   f"<td style=\"border:1px solid #dddddd;\">{item.product}</td>" \
                   f"<td style=\"border:1px solid #dddddd;\">{item.packaging}</td>" \
                   f"<td style=\"border:1px solid #dddddd;\">{item.price} грн</td>" \
                   f"<td style=\"border:1px solid #dddddd;\">{item.quantity}</td>" \
                   f"<td style=\"border:1px solid #dddddd;\">{item.get_total_price()} грн</td>" \
                   f"</tr>"
    message += "</table> <br>"

    message += f"<b>Сума замовлення:</b> {order.order_sum} грн<br>"
    if order.order_discount != 0:
        message += f"Знижка: {order.order_discount} грн<br>"
    message += f"<b><span style=\"font-size: 130%;\">ДО СПЛАТИ:{order.order_sum_w_discount} грн</span></b> <br>"

    message += "<hr>"
    message += f"<b>Покупець:</b> {order.user.first_name} {order.user.last_name}<br>"
    message += f"<b>Телефон:</b> {order.user.phone_number}<br>"
    message += f"<b>Email:</b> {order.user.email}<br>"
    message += f"<b>Спосіб доставки:</b> {order.delivery_method}<br>"
    message += f"<b>Місто:</b> {order.city}<br>"
    message += f"<b>Відділення(адреса):</b> {order.post_department}<br>"
    message += f"<b>Спосіб оплати:</b> {order.payment_method}<br>"
    if order.comment:
        message += f"<b>Коментар:</b> {order.comment}<br>"

    return message

