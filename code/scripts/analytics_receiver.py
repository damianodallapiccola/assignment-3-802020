import pika
import json

rabbit_uri = 'amqp://guest:guest@localhost/'
params = pika.URLParameters(rabbit_uri)
queue = 'analytics_streaming'

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue=queue)

def callback(ch, method, properties, body):
    data = json.loads(body)
    # TODO: add logs
    print(data)

channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

