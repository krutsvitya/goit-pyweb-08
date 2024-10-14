import pika
import mongoengine as me
from models import Contact

me.connect(host="mongodb+srv://krutsvitya:vitya091003@krutsvitya.plhxk.mongodb.net/test?retryWrites=true&w=majority"
                "&appName=krutsvitya")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')


def send_email_stub(contact):
    print(f"Имитируем отправку email для {contact.fullname} на адрес {contact.email}")
    return True


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()

    if contact and not contact.message_sent:
        if send_email_stub(contact):
            contact.message_sent = True
            contact.save()
            print(f"Email отправлен контакту {contact.fullname}, статус обновлен.")
        else:
            print(f"Ошибка отправки email для {contact.fullname}.")


channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Ожидание сообщений. Для выхода нажмите CTRL+C')
channel.start_consuming()
