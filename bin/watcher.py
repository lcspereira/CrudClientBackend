import pika
import time
from utils.message_queue import Consumer


def on_message(channel, method_frame, header_frame, body):
    """Callback para processamento de mensagem recebida"""
    print(body.decode("utf8"))
    print("processando...")
    time.sleep(5)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == "__main__":
    consumer = Consumer("crud", "crud", "crud")
    consumer.consume(on_message)
