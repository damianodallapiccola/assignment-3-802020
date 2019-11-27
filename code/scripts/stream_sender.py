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
channel.queue_declare(queue=queue)

# channel_report = connection.channel()
# channel_report.queue_declare(queue="reports")


def main():

    file_path = sys.argv[1]
    # config_file_path = sys.argv[2]

    # with open(config_file_path, 'r') as f:
    #     parsed_json = json.load(f)


    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                # data to be sent to api
                part_id = row[0]
                ts_date = row[1]
                ts_time = row[2]
                room = row[3]
                json_to_send ={'part_id': int(part_id), 'ts_date': ts_date, 'ts_time': ts_time, 'room': room}
                sleep(0.1*randint(1, 20))
                channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(json_to_send))
                print("Line " + str(line_count) + " published")
                line_count += 1


if __name__ == "__main__":
    main()
