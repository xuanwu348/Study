#encoding:utf-8
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')


#The queue name needs to be specified in the routing_key parameter
channel.basic_publish(exchange="",
        routing_key="hello",
        body="Hello World")
print("[x] Sent 'hello world'")
connection.close()

