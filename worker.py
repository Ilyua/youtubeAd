import pika
import time
import sys
import random
from  main import main
from key_phrase_parser import parse_feq_dictionary

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print (' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received ")
    main(body)
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)#?

channel.basic_qos(prefetch_count=1)#Чтобы не отдавал воркеру все сразу, атолько после подтверждения
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
