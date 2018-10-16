#encoding:utf-8
import pika
import signal

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="logs",
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print("[*]Waiting for logs. To eixt press CTRL+C")

def callback(ch, method, properties, body):
    print("[x] %r" % body)

def myhandle(num, frame):
    exit()

signal.signal(signal.SIGINT, myhandle)
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()

