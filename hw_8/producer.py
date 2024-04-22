import pika
from mongoengine import connect, Document, StringField, BooleanField
from faker import Faker

# Підключення до MongoDB
connect('email_contacts')

# Оголошення моделі для контакту
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='email_queue')

# Генерування фейкових контактів та їх запис у базу даних та відправка ID у чергу
fake = Faker()
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    contact = Contact(fullname=fullname, email=email)
    contact.save()
    channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))

print("Фейкові контакти збережено та відправлено у чергу")

connection.close()
