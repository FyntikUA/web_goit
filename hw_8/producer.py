import pika
from mongoengine import connect, Document, StringField, BooleanField
from faker import Faker

# Підключення до MongoDB
connect('contacts_db')

# Оголошення моделі для контакту
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField()
    prefered_contact_method = StringField(choices=['SMS', 'email'], default='email')
    message_sent = BooleanField(default=False)

# Параметри з'єднання з RabbitMQ
rabbitmq_connection_parameters = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(rabbitmq_connection_parameters)
channel = connection.channel()

# Створення черг для SMS та email
channel.queue_declare(queue='sms_contacts')  # Черга для SMS
channel.queue_declare(queue='email_contacts')  # Черга для email

# Отримання контактів з бази даних та розміщення їх у відповідні черги
for contact in Contact.objects:
    if contact.prefered_contact_method == 'SMS':
        # Відправка ID контакту в чергу для SMS
        channel.basic_publish(exchange='', routing_key='sms_contacts', body=str(contact.id))
    else:
        # Відправка ID контакту в чергу для email
        channel.basic_publish(exchange='', routing_key='email_contacts', body=str(contact.id))

# Генерування фейкових контактів, їх запис у базу даних та відправка ID у чергу для email
fake = Faker()
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    contact = Contact(fullname=fullname, email=email)
    contact.save()
    # Відправка ID нового контакту в чергу для email
    channel.basic_publish(exchange='', routing_key='email_contacts', body=str(contact.id))

print("Фейкові контакти збережено та відправлено у черги")

# Закриття з'єднання з RabbitMQ
connection.close()
