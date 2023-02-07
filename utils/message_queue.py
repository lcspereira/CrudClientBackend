import pika


class MessageQueueBase(object):
    url: pika.URLParameters = pika.URLParameters("amqp://localhost:5672/")
    conn: pika.BlockingConnection
    channel: pika.adapters.blocking_connection.BlockingChannel
    exchange: str
    queue: str = None
    routing_key: str

    def __init__(self, exchange: str, queue: str, routing_key: str) -> None:
        self.conn = pika.BlockingConnection(self.url)
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key
        self.channel = self.conn.channel()
        self.channel.queue_declare(self.queue, durable=False, auto_delete=True)
        self.channel.exchange_declare(self.exchange, durable=False, auto_delete=True)
        self.channel.queue_bind(self.queue, self.exchange)


class Publisher(MessageQueueBase):
    def publish(self, msg: str) -> None:
        """Publica mensagem na fila

        Args:
            msg (str): Mensagem a ser publicada
        """
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=msg,
        )


class Consumer(MessageQueueBase):
    def consume(self, callback):
        """Inicia consumo da fila de mensagens

        Args:
            callback (function): Função de processamento de mensagem
        """
        self.channel.basic_consume("crud", callback)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt as ex:
            self.channel.stop_consuming()
        finally:
            self.channel.close()
