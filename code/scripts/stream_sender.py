import sys
import pika
import os
from time import sleep
import logging


log_format = '%(asctime)s : [%(levelname)s] - %(message)s'
logs_directory = "../../logs/stream_sender.log"
logs_dir_full_path = os.path.abspath(logs_directory)
logging.basicConfig(filename= logs_dir_full_path , filemode="a", level= logging.INFO, format=log_format)


#rabbit_uri = 'amqp://guest:guest@localhost/'
rabbit_uri = 'amqp://vsvgiedg:1T2CYKC2bwIYhKAXN8H1Xn0FNwguWAGB@hawk.rmq.cloudamqp.com/vsvgiedg'

params = pika.URLParameters(rabbit_uri)
queue = 'data_streaming'

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)


def main():

    file_path = sys.argv[1]

    with open(file_path) as fp:
        for cnt, line in enumerate(fp):
            sleep(0.005)
            channel.basic_publish(exchange='', routing_key=queue, body=line)
            logging.info("Line {} sent: {}".format(cnt, line))
            print("Line {}: {}".format(cnt, line))


if __name__ == "__main__":
    main()
