import pika
import uuid
import sys

class FibnacciRPCClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="cmd",
                                 exchange_type='fanout')
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response,
                                   queue=self.callback_queue,
                                   no_ack=True)

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, command):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange="cmd",
                                   routing_key='',
                                   properties=pika.BasicProperties(
                                       reply_to = self.callback_queue,
                                       correlation_id = self.corr_id,
                                       ),
                                   body=command)
        while self.response is None:
            self.connection.process_data_events()
            if self.response:
                print(self.response.decode("utf-8"))
        #return self.response.decode("utf-8")
while 1:
    fibonacci_rpc = FibnacciRPCClient()
    command = input("please input a command:")
    if not command:
        continue
    elif command == 'q':
        sys.exit(0)
    else:
        command = command
    print("[x] Send command {}".format(command))
    response = fibonacci_rpc.call(command)
    #print("[.]Got\n %s" % response)
            
                                   
