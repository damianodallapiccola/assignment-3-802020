from pymongo import MongoClient
import sys
import csv
import json
import pika
from random import randint
from time import sleep



rabbit_uri = 'amqp://guest:guest@localhost/'
params = pika.URLParameters(rabbit_uri)
queue = 'data_streaming'

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)

# channel_report = connection.channel()
# channel_report.queue_declare(queue="reports")


def main():

    file_path = sys.argv[1]
    # config_file_path = sys.argv[2]

    # with open(config_file_path, 'r') as f:
    #     parsed_json = json.load(f)

    with open(file_path) as fp:
        for cnt, line in enumerate(fp):
            # sleep(0.005)
            channel.basic_publish(exchange='', routing_key=queue, body=line)
            print("Line {}: {}".format(cnt, line))



if __name__ == "__main__":
    main()
