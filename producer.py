import pika
import mongoengine as me
from models import Contact
from faker import Faker

me.connect(host="mongodb+srv://krutsvitya:vitya091003@krutsvitya.plhxk.mongodb.net/test?retryWrites=true&w=majority"
                "&appName=krutsvitya")

fake = Faker()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')


def generate_contacts(count):
    for _ in range(count):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number()
        )
        contact.save()
        channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))
        print(f"Отправлено сообщение для контакта {contact.fullname} с ID {contact.id}")


generate_contacts(10)

connection.close()
