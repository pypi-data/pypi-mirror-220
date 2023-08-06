# Copyright: 北京物元数界科技有限公司
# Author: 邵芒
# Contact: 微信 stormx

import random
from pdb import set_trace as stop

from paho.mqtt import client as mqtt_client
from paho.mqtt.properties import Properties, PacketTypes
import threading, time
from metathing.logger import logger

class Mqtt():
    def __init__(self, broker: str = '127.0.0.1', port: int = 1883, ws_addr: str = None, ws_port = 8083) -> None:
        self.broker = broker
        self.port = port
        self.client = None
        self.client_2 = None
        self.resp_topic = "/resp/{0}".format(random.randint(0, 999999999999))
        self.ws_addr = ws_addr
        self.ws_port = ws_port

    def connect(self):
        def on_connect(client, userdata, flags, rc, properties=None):
            if rc == 0:
                logger.info("Connected: {0}".format(client._client_id.decode()))
                pass
            else:
                logger.error("Failed to connect, return code %d\n" % rc)
        if self.ws_addr is not None:
            self.client = mqtt_client.Client(
                f'ws-srv-{random.randint(0, 99999999999)}', protocol=5, transport="websockets")
            self.client_2 = mqtt_client.Client(
                f'ws-srv2-{random.randint(0, 99999999999)}', protocol=5, transport="websockets")
            logger.info("WebSocket ID: {0}".format(self.client._client_id.decode()))
            self.client.on_connect = on_connect
            self.client.ws_set_options(path='/mqtt')
            self.client_2.ws_set_options(path='/mqtt')
            try:
                self.client.connect(self.ws_addr, port=self.ws_port)
                self.client_2.connect(self.ws_addr, port=self.ws_port)
            except:
                time.sleep(1)
                self.client.connect(self.ws_addr, port=self.ws_port)
                self.client_2.connect(self.ws_addr, port=self.ws_port)
        else:
            self.client = mqtt_client.Client(
                f'mqtt-srv-{random.randint(0, 99999999999)}', protocol=5)
            self.client_2 = mqtt_client.Client(
                f'mqtt-srv2-{random.randint(0, 99999999999)}', protocol=5)
            logger.info("MQTT ID: {0}".format(self.client._client_id.decode()))
            self.client.on_connect = on_connect
            try:
                self.client.connect(self.broker, self.port)
                self.client_2.connect(self.broker, self.port)
            except:
                time.sleep(1)
                self.client.connect(self.broker, self.port)
                self.client_2.connect(self.broker, self.port)
        self.client.subscribe(self.resp_topic, 1, properties=Properties(PacketTypes.SUBSCRIBE))
        self.client.loop_start()
        
        self.client_2.subscribe(self.resp_topic, 1, properties=Properties(PacketTypes.SUBSCRIBE))
        self.client_2.loop_start()

    def publish(self, topic: str, content: str, qos: int = 0, retain: bool = False, properties=Properties(PacketTypes.PUBLISH)):
        self.client_2.publish(topic, content, qos, retain, properties=properties)

    # Sync
    # def publish_request(self, topic: str, content: str, qos: int = 0, timeout = 5, retain: bool = False):
    #     resp_lock = threading.Lock()
    #     resp_lock.acquire()
    #     properties = Properties(PacketTypes.PUBLISH)
    #     properties.ResponseTopic = self.resp_topic
    #     self.resp = None
        
    #     def on_response(client, userdata, msg):
    #         self.resp = msg.payload.decode('utf-8')
    #         self.client.message_callback_remove(self.resp_topic)
    #         if resp_lock.locked():
    #             resp_lock.release()
        
    #     self.client.message_callback_add(self.resp_topic, on_response)
    #     # Send the request
    #     self.client.publish(topic, content, qos, retain, properties=properties)
    #     resp_lock.acquire(blocking=True, timeout=timeout)
    #     if resp_lock.locked():
    #         resp_lock.release()
    #     return self.resp
        

    def publish_request(self, topic: str, content: str, qos: int = 0, timeout = 5, retain: bool = False):
        try:
            resp_lock = threading.Lock()
            resp_lock.acquire()
            properties = Properties(PacketTypes.PUBLISH)
            properties.ResponseTopic = self.resp_topic
            self.resp = None
            
            def on_response(client, userdata, msg):
                self.resp = msg.payload.decode('utf-8')
                self.client_2.message_callback_remove(self.resp_topic)
                if resp_lock.locked():
                    resp_lock.release()
                else:
                    logger.warning("Message reached but lock is timeout! （考虑缩短下游耗时或提高超时时间？）")
            
            self.client_2.message_callback_add(self.resp_topic, on_response)
            # Send the request
            self.client_2.publish(topic, content, qos, retain, properties=properties)
            resp_lock.acquire(blocking=True, timeout=timeout)
            if resp_lock.locked():
                resp_lock.release()
            return self.resp
        except Exception as e:
            logger.Error(e)
        
    # NEED TEST
    def publish_request_async(self, res, topic: str, content: str, qos: int = 0, timeout = 5, retain: bool = False):
        properties = Properties(PacketTypes.PUBLISH)
        properties.ResponseTopic = self.resp_topic
        self.resp = None
        def on_response(client, userdata, msg):
            self.resp = msg.payload.decode('utf-8')
            self.client_2.message_callback_remove(self.resp_topic)
            res = self.resp
        self.client_2.message_callback_add(self.resp_topic, on_response)
        self.client_2.publish(topic, content, qos, retain, properties=properties)
        

    # Accept list, e.g. subscribe([("my/topic", 0), ("another/topic", 2)])
    def subscribe(self, topic, qos: int = 1):
        if (isinstance(topic, list)):
            self.client.subscribe(topic, qos, properties=Properties(PacketTypes.SUBSCRIBE))
            # for t in topic:
            #     print("Subscribe to %s" % t)
        else:
            # print("Subscribe to %s" % topic)
            self.client.subscribe(topic, qos, properties=Properties(PacketTypes.SUBSCRIBE))

    def unsubscribe(self, topic):
        # print("Unsubscribe %s" % topic)
        self.client.unsubscribe(topic)

    def message_callback_add(self, topic: str, callback):
        # print("Add callback to topic %s" % topic)
        self.client.message_callback_add(topic, callback)

    def message_callback_remove(self, topic: str):
        # print("Remove callback to topic %s" % topic)
        self.client.message_callback_remove(topic)

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT Broker: %s:%s!" %
              (self.broker, self.port))
