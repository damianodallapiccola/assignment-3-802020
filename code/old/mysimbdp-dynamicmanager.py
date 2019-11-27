import pika
import json
import os
import logging

log_format = '%(asctime)s : [%(levelname)s] - %(message)s'

logs_directory = "../logs/mysimbdp-dynamicmanager.log"
logs_dir_full_path = os.path.abspath(logs_directory)

logging.basicConfig(filename= logs_dir_full_path , filemode="a", level= logging.INFO, format=log_format)

# initialization of the two clients
os.system("python3 mysimbdp-streamingestmanager.py client1 start")
os.system("python3 mysimbdp-streamingestmanager.py client2 start")




# rabbit_uri = "amqp://vsvgiedg:1T2CYKC2bwIYhKAXN8H1Xn0FNwguWAGB@hawk.rmq.cloudamqp.com/vsvgiedg"
rabbit_uri = 'amqp://guest:guest@localhost/'
params = pika.URLParameters(rabbit_uri)
queue = "reports"
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue=queue)


def callback(ch, method, properties, body):
    data = json.loads(body)
    client_id = data["client_id"]
    proc_rate = data["proc_rate"]
    avg_ingest_time = data["avg_ingest_time"]
    tot_data_size = data["tot_data_size"]
    n_mess = data["n_mess"]
    print("report " + str(client_id) + "- proc_rate: " + str(proc_rate) + ", avg_ingest_time: " + str(avg_ingest_time) + ", tot_data_size: " + str(tot_data_size) + ", n_mess: " + str(n_mess))
    logging.info("report " + str(client_id) + "- proc_rate: " + str(proc_rate) + ", avg_ingest_time: " + str(avg_ingest_time) + ", tot_data_size: " + str(tot_data_size) + ", n_mess: " + str(n_mess))
    if(n_mess > 30):
        os.system("python3 mysimbdp-streamingestmanager.py " + str(client_id) + " " + "start")
        print("process " + str(client_id) +  " automatically added")
        logging.info("process " + str(client_id) +  " automatically added")
    if(n_mess < 5):
        os.system("python3 mysimbdp-streamingestmanager.py " + str(client_id) + " " + "stop")
        print("process " + str(client_id) +  " automatically removed")
        logging.info("process " + str(client_id) + " automatically removed")

channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()