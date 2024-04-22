import pika
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect('email_contacts')

# Функція-заглушка для надсилання email
def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Надсилаємо email на адресу {contact.email} для {contact.fullname}")
        contact.sent = True
        contact.save()

# Обробка повідомлень з черги
def callback(ch, method, properties, body):
    contact_id = body.decode()
    send_email(contact_id)
    print(f"Повідомлення для контакту з ID {contact_id} оброблено")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='email_queue')

# Встановлення функції зворотного виклику для обробки повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Очікування повідомлень. Для виходу натисніть CTRL+C')

# Початок прослуховування черги
channel.start_consuming()
