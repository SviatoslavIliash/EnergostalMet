import requests
from django.core.mail import send_mail
from django.conf import settings
@staticmethod
def send_telegram(order, order_items):
    message = telegram_message(order, order_items)

    TOKEN = ""
    chatId = ''
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

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
def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    send_mail(subject, message, email_from, recipient_list)