#encoding:utf-8
import pika
import os
import signal
import random

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange="cmd",
                         exchange_type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='cmd',
                   queue=queue_name)

channel.queue_declare(queue='rpc_queue')

def fib(command):
    output = os.popen(command)
    output = "{} {}".format(random.randint(0,100000),"\n") + output.read()
    print(output)
    return output

def myhandle(num, frame):
    exit()

def on_request(ch, method, properties, body):
    command = body.decode("utf-8")

    print("[.] execute command 'df -h'")
    response = fib(command)
    print(response)
    ch.basic_publish(exchange="",
                     routing_key=properties.reply_to,
                     properties = pika.BasicProperties(correlation_id = \
                                                       properties.correlation_id),
                     body = str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count = 1)
channel.basic_consume(on_request,
                      queue=queue_name)
signal.signal(signal.SIGINT, myhandle)
print("[x]Awaiting RPC request")
channel.start_consuming()
