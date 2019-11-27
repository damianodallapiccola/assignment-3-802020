from flask import Flask
from flask import request
import pika
import json
import os
import logging

log_format = '%(asctime)s : [%(levelname)s] - %(message)s'

logs_directory = "../logs/mysimbdp-databroker.log"
logs_dir_full_path = os.path.abspath(logs_directory)

logging.basicConfig(filename= logs_dir_full_path , filemode="a", level= logging.INFO, format=log_format)

app = Flask(__name__)

# rabbitmq_uri = 'amqp://vsvgiedg:1T2CYKC2bwIYhKAXN8H1Xn0FNwguWAGB@hawk.rmq.cloudamqp.com/vsvgiedg'
rabbitmq_uri = 'amqp://guest:guest@localhost/'
params = pika.URLParameters(rabbitmq_uri)




@app.route('/upload', methods=['POST'])
def add_location():
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    request_body = request.json
    user_id = request_body["user_id"]
    data = request_body["data"]
    print(request_body)
    logging.info("data ingested:  " + str(request_body))
    channel.queue_declare(queue=user_id)
    channel.basic_publish(exchange='', routing_key=user_id, body=json.dumps(data))
    channel.close()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


if __name__ == '__main__':
    app.run(debug=True)

