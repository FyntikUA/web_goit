import pika
from mongoengine import connect
from models import Contact

# Підключення до бази даних MongoDB
connect('contacts_db')

# Параметри з'єднання з RabbitMQ
rabbitmq_connection_parameters = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(rabbitmq_connection_parameters)
channel = connection.channel()

# Створення черги для email
channel.queue_declare(queue='email_contacts')

def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects.get(id=contact_id)
    # Тут можна реалізувати логіку відправки email
    print(f"Email sent to {contact.fullname}")
    # Позначаємо, що повідомлення надіслано
    contact.message_sent = True
    contact.save()

# Встановлення функції зворотного виклику для обробки повідомлень з черги email
channel.basic_consume(queue='email_contacts', on_message_callback=callback, auto_ack=True)

print('Waiting for email contacts. To exit press CTRL+C')
channel.start_consuming()
