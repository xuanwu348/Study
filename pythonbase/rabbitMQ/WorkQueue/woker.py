#encoding:utf-8
import time
import pika
import signal

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    print("[x]receive %r" % body)
    time.sleep(body.count(b'.'))
    print("[x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

def myHandle(num, frame):
    exit()

channel.basic_consume(callback, 
        queue='task_queue',
        #no_ack=True
        )

signal.signal(signal.SIGINT, myHandle)
print("[*] Waiting for messages, To exit press CTRL+C")
channel.start_consuming()



