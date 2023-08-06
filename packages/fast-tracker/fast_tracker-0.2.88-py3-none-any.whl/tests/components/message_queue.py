#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    Created by wangl10@mingyuanyun.com on 2017/8/9.
"""
import logging
import pika
import socket
import struct
import threading
import time
from pika.adapters.blocking_connection import BlockingConnection
from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials

from tests.libs import config


class RabbitMQ:
    def __init__(self, host=None, port=None, user=None, password=None, heartbeat=None):
        self.lock = threading.Lock()
        self.host = host or config.get("RabbitMQ.host", self._loopback_address)
        self.port = port or int(config.get("RabbitMQ.port", 5672))
        self.user = user or config.get("RabbitMQ.user", "guest")
        self.password = password or config.get("RabbitMQ.password", "guest")
        self.heartbeat = heartbeat or config.get("RabbitMQ.heartbeat", 60)

    @property
    def _loopback_address(self):
        return socket.inet_ntoa(struct.pack("!I", socket.INADDR_LOOPBACK))

    def get_connection(self):
        """
        获取BlockingConnection
        :return:pika.adapters.blocking_connection.BlockingConnection
        """
        credentials = PlainCredentials(self.user, self.password)
        return BlockingConnection(
            parameters=ConnectionParameters(self.host, self.port, credentials=credentials, heartbeat=self.heartbeat)
        )

    def send_message(self, queue, body, durable=True):
        """
        发送消息
        :param str queue: 队列名称
        :param str body: 消息内容
        :param bool durable: 消息是否持久
        :return:
        """
        with self.get_connection() as connection:
            print(int(getattr(connection, "_impl").params.heartbeat / 2))
            channel = connection.channel()
            channel.queue_declare(queue=queue, durable=durable)
            return channel.basic_publish(
                exchange="", routing_key=queue, body=body, properties=pika.BasicProperties(delivery_mode=2)
            )

    def receive_message(self, queue, consumer_callback, durable=True):
        """
        接收消息
        :param str queue: 队列名称
        :param function consumer_callback:处理消息函数
        :param bool durable: 消息是否持久
        :return:
        """
        while True:
            try:
                connection = self.get_connection()
                logging.info("心跳时间{}".format((getattr(connection, "_impl").params.heartbeat)))
                channel = connection.channel()
                channel.queue_declare(queue=queue, durable=durable)
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue, consumer_callback, auto_ack=False)
                channel.start_consuming()
            except Exception as e:
                connection.close()
                logging.error(f"失去连接: {e}")

    def queue_delete(self, queue):
        """
        删除队列
        :param str queue:队列名称
        :return:
        """
        with self.get_connection() as connection:
            channel = connection.channel()
            channel.queue_delete(queue=queue)

    def get_consumer_count(self, queue):
        """
        获取队列总数
        :param queue:
        :return:
        """
        with self.get_connection() as connection:
            channel = connection.channel()
            this = channel.queue_declare(queue=queue)
            return this.method.consumer_count


class Heartbeat(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.lock = threading.Lock()
        self.connection = connection
        self.heartbeat = int(getattr(connection, "_impl").params.heartbeat / 2)
        self.setDaemon(True)
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while self._running:
            time.sleep(self.heartbeat)
            self.lock.acquire()
            try:
                logging.info("发送心跳……")
                self.connection.process_data_events()
            except Exception as ex:
                logging.error("Error format:" + str(ex))
            finally:
                self.lock.release()
