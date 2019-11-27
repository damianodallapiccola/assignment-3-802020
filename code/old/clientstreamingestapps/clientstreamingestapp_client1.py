import pika
import json
from pymongo import MongoClient
import sys
from datetime import datetime

config_file_path = sys.argv[1]

with open(config_file_path, 'r') as f:
    parsed_json = json.load(f)

mongo_uri = parsed_json['mongo_uri']
mongo_dbname = parsed_json['mongo_db_name']

client = MongoClient(mongo_uri)
db = client[mongo_dbname]

rabbit_uri = parsed_json['rabbit_uri']
queue = parsed_json['queue']
params = pika.URLParameters(rabbit_uri)
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue=queue)

channel_report = connection.channel()
channel_report.queue_declare(queue="reports")

ingestion_time = []
data_sizes = []
time_interval = 30
count = 0

def callback(ch, method, properties, body):
    ti = datetime.timestamp(datetime.now())
    data = json.loads(body)
    db.indoorLocalization.insert_one(data)
    tf = datetime.timestamp(datetime.now())
    ingestion_time.append(tf-ti)
    data_sizes.append(sys.getsizeof(data))


channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()

while channel._consumer_infos:
    channel._process_data_events(time_limit=1)
    count += 1
    if count == time_interval:
        if len(ingestion_time) != 0:
            # print("processing rate (Byte/time_interval): "+str((sum(data_sizes)/8)/time_interval))
            # print("Average ingestion time (s): " + str(sum(ingestion_time)/len(ingestion_time)))
            # print("total (Byte): " + str(sum(data_sizes)/8))
            # print("n messagges: "+str(len(data_sizes)))
            report = {
                "client_id": str(queue),
                "proc_rate": sum(data_sizes)/time_interval,
                "avg_ingest_time": sum(ingestion_time)/len(ingestion_time),
                "tot_data_size": sum(data_sizes),
                "n_mess": len(data_sizes)
            }
            ingestion_time = []
            data_sizes = []
        else:
            report = {
                "client_id": str(queue),
                "proc_rate": 0,
                "avg_ingest_time": 0,
                "tot_data_size": 0,
                "n_mess": 0
            }

        channel_report.basic_publish(exchange='', routing_key="reports", body=json.dumps(report))
        count = 0