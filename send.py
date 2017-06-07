import pika
import sys
from key_phrase_parser import parse_feq_dictionary
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
for i,phrase in enumerate(list(parse_feq_dictionary('5000lemma.txt'))):
    if i > 4:
        break
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=phrase,
                          properties=pika.BasicProperties(
                             delivery_mode = 2, # make message persistent
                          ))
    print(" [x] Sent {}".format(phrase))
connection.close()
