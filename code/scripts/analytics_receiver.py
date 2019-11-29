import pika
import os
import logging

log_format = '%(asctime)s : [%(levelname)s] - %(message)s'
logs_directory = "../../logs/analytics_receiver.log"
logs_dir_full_path = os.path.abspath(logs_directory)
logging.basicConfig(filename= logs_dir_full_path , filemode="a", level= logging.INFO, format=log_format)



# rabbit_uri = 'amqp://guest:guest@localhost/'
rabbit_uri = 'amqp://vsvgiedg:1T2CYKC2bwIYhKAXN8H1Xn0FNwguWAGB@hawk.rmq.cloudamqp.com/vsvgiedg'
params = pika.URLParameters(rabbit_uri)
queue = 'analytics_streaming'

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue=queue)

def callback(ch, method, properties, body):
    logging.info("Analytics received: {}".format(body))
    print(body)

channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

