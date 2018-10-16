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

#n order to defeat that we can use the basic.qos method with the prefetch_count=1 setting. This tells RabbitMQ not to give more than one message to a worker at a time. Or, in other words, don't dispatch a new message to a worker until it has processed and acknowledged the previous one. Instead, it will dispatch it to the next worker that is not still busy.
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, 
        queue='task_queue',
        #no_ack=True
        )

signal.signal(signal.SIGINT, myHandle)
print("[*] Waiting for messages, To exit press CTRL+C")
channel.start_consuming()



