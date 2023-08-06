# Copyright: 北京物元数界科技有限公司
# Author: 邵芒
# Contact: 微信 stormx

import json
from pdb import set_trace as stop

from tornado.escape import json_decode
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.routing import (AnyMatches, DefaultHostMatches, HostMatches,
                             ReversibleRouter, ReversibleRuleRouter, Rule,
                             URLSpec, _RuleList)
from tornado.web import Application, RequestHandler, _ApplicationRouter
from .mqtt import Mqtt
from functools import partial
import inspect
import sys

from metathing.logger import logger

# from .alarmer import Alarmer, Err

class CustomHandler(RequestHandler):
    def get_argument(self, id: str):
        if self.request.headers['Content-Type'] == 'application/json':
            args = json_decode(self.request.body)
            return args[id]
        return super(CustomHandler, self).get_argument(id)

    def get_argument_dict(self):
        params = self.request.arguments
        for k, v in params.items():
            params[k] = v[0].decode("utf-8")
        return params

# Base for protocol service


class Device():
    def __init__(self, srv, model) -> None:
        self.config = srv.config
        self.srv_name = srv.srv_name
        # self.resources = {}
        self.event_sender = {}
        if isinstance(model, str):
            self.model = json.loads(model)
        else:
            self.model = model

        self.srv = srv
        self.mqtt = Mqtt(srv.config['MQTT_ADDR'], srv.config['MQTT_PORT'])
        self.mqtt.connect()
        # self.cb_stack = {}
        
        for k, v in self.model.items():
            setattr(self, k, v)
            
        # self.alarmer = None
        self._dev_id = model['dev_id']
        self.Build()

            # if 'srv_type' in model:
            #     self.srv_type = model['srv_type']
            # else:
            #     self.srv_type = "Device"

            # if 'label' in model:
            #     self.label = model['label']
            # else:
            #     self.label = "N/A"

            # self.alarmer = Alarmer(self.mqtt.broker, self.mqtt.port)
            # self.alarmer.connect(self.srv_name, self._dev_id,
            #                      self.label, self.srv_type)

        # self.dev_srvs = {}
        # if 'services' in model:
        #     for s in model['services']:
        #         self.dev_srvs[s['id']] = s

    # def initialize(self):
    #     raise NotImplementedError

    #region Built-in funcs
    def DevInfo(self):
        return {'info': self.model}
    
    def Event(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            fn_name = func.__name__
            if fn_name in self.event_sender:
                for topic in self.event_sender[fn_name]:
                    self.srv.mqtt.publish(topic, json.dumps(result))
            return result
        wrapper.__is_event__ = func
        return wrapper
    
        
    def BindAction(self, model):
        fn_name = model['tag']
        # Check action
        if hasattr(self, fn_name) == False:
            logger.error("Device Action not found [{0}]".format(fn_name))
            return False
        fn = getattr(self, fn_name)
        
        # Process overrides
        vo_map = {}
        if 'var_override' in model:
            for vo in model['var_override']:
                vo_map[vo['var_uid']] = vo['default']
                
        input_args = list(inspect.signature(fn).parameters.keys())
        input_args_const = {}
        # Check inputs
        for arg in model['srv_input']:
            if not arg['var_tag'] in input_args:
                logger.error("Input not found [{0}]".format(arg['var_tag']))
                return False
            arg['is_constant'] = arg['uid'] in vo_map
            if arg['is_constant']:
                v = self._dtype_cast(arg['dtype'], vo_map[arg['uid']])  
                input_args_const[arg['var_tag']] = v
            else: 
                self._dtype_cast(arg['dtype'], arg['default'])
        
        # Generate lambda that replace input with default value if is_constant
        if len(input_args_const) > 0:
            new_fn = partial(fn, **input_args_const)
        else:
            new_fn = fn
        
        # Subscribe to new topic
        self.srv.mqtt.subscribe(model['topic'])
        def callback (client, userdata, msg):
            try:
                message = []
                payload = msg.payload.decode('utf-8')
                inputs = json.loads(payload)
                res = new_fn(**inputs)
                message.append(f"-= {msg.topic} =-")
                message.append(f"- In -")
                for k, v in inputs.items():
                    message.append(f"{k}: {v}")
                message.append(f"- Out -")
                if res is not None:
                    for k,v in res.items():
                        message.append(f"{k}: {v}")
                    if hasattr(msg, 'properties') and hasattr(msg.properties, 'ResponseTopic'):
                        message.append(f"- ResponseTopic -")
                        message.append(f"{msg.properties.ResponseTopic}")
                        self.srv.mqtt.publish(msg.properties.ResponseTopic, json.dumps(res))
                self.srv.app._print_frame(message)
            except Exception as e:
                logger.error(e)
        self.srv.mqtt.message_callback_add(model['topic'], callback)
        return True
    
    def BindEvent(self, model):
        fn_name = model['tag']
        # Check action
        if hasattr(self, fn_name) == False:
            logger.error("Event not found [{0}]".format(fn_name))
            return False
        
        if fn_name in self.event_sender:
            self.event_sender[fn_name].append(model['topic'])
        else:
            self.event_sender[fn_name] = [model['topic']]
        return True
    
    @staticmethod
    def _dtype_cast(dtype: str, item: str):
        if dtype == 'int':
            return int(item)
        elif dtype == 'float':
            return float(item)
        elif dtype == 'bool':
            if item == 'true':
                return True
            else:
                return False
        return item
    
              
    #endregion

    def Build(self):
        self.appList = [
            ('/{0}/devices/{1}/ping'.format(self.srv_name, self._dev_id), Ping),
            # ('/{0}/devices/{1}/resources/(.*)'.format(self.srv_name,
            #  self._dev_id), DevProperty, dict(dev=self, srv=self.srv)),
            # ('/{0}/devices/{1}/services/(.*)'.format(self.srv_name,
            #  self._dev_id), DevService, dict(dev=self, srv=self.srv)),
            # ('/{0}/devices/{1}/events/(.*)'.format(self.srv_name,
            #  self._dev_id), DevEvent, dict(dev=self, srv=self.srv)),
            ('/{0}/devices/{1}/selectors/(.*)'.format(self.srv_name,
             self._dev_id), DevSelector, dict(dev=self, srv=self.srv)),
            # ('/{0}/devices/{1}/mqtt/(.*)'.format(self.srv_name,
            #  self._dev_id), DevMqttOp, dict(dev=self, srv=self.srv)),
        ]
        
        if self.config['PORT'] < 65535:
            # 0.1.19 Fix release handlers
    #        self.srv.http.httpApp.add_handlers(r".*", self.appList)
            host_matcher = HostMatches(r".*")
            self.rule = Rule(host_matcher, _ApplicationRouter(
                self.srv.http.httpApp, self.appList))
            self.srv.http.httpApp.default_router.rules.insert(-1, self.rule)
            
        # 0.1.20 MQTT support
        topic = '/{0}/devices/{1}/selectors/#'.format(self.srv_name, self._dev_id)
        self.mqtt.subscribe(topic)
        def callback (client, userdata, msg):
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            # check response
            func_name = topic.split('/')[5]
            res = self.selector(func_name, payload)
            message = [
                "Message received: {0} - {1}".format(topic, payload),
                "Response: {0}".format(res)
            ]
            
            # Check responseTopic exists
            if hasattr(msg, 'properties') and hasattr(msg.properties, 'ResponseTopic'):
                self.mqtt.publish(msg.properties.ResponseTopic, json.dumps(res))
        self.mqtt.message_callback_add(topic, callback)

    def release(self):
        self.srv.http.httpApp.default_router.rules.remove(self.rule)
        return {}

    # Selector
    def selector(self, func_name: str, content=None):
        try:
            if (content == None or content == '{}'):
                return getattr(self, func_name)()
            else:
                if isinstance(content, str):
                    return getattr(self, func_name)(**(json.loads(content)))
                elif isinstance(content, dict):
                    try:
                        return getattr(self, func_name)(**content)
                    except:
                        return getattr(self, func_name)(content)
                else:
                    # self.alarmer.alarm(Err.SRV_REQ_INVALID, 1,
                                    # "f:%{0} - {1}".format(func_name, content))
                    logger.error("f:%{0} - {1}, Content type is not supported").format(func_name, content)
                    return "Content type is not supported"
        except Exception as e:
            logger.error("Selector error: %s" % e)
            return "Selector error: %s" % e

    # def service(self, srv_name: str, content=None):
    #     if self.dev_srvs is None:
    #         return "Device has no service"
    #     if srv_name in self.dev_srvs:
    #         srv_model = self.dev_srvs[srv_name]
    #         func_name = srv_model['selector']
    #         return self.selector(func_name, content)
    #     else:
    #         # self.alarmer.alarm(Err.SRV_NO_EXIST, 1, srv_name)
    #         return "Device does not have service: %s" % srv_name

    def ping(self):
        return "OK"
    
    # 【弃用管道】
    # def flow(self, op: str, srv_name='', sub_topic: str = None, pub_topic: str = None, qos=1):
    #     qos = int(qos)
    #     print("Add flow, dev addr: {0}".format(self))
    #     # Automate: sub func input, pub func output
    #     if (op == "add"):
    #         if (sub_topic != None):
    #             self.mqtt.subscribe(sub_topic, qos)

    #         # Inject constants
    #         constants = {}
    #         try:
    #             constants = json.loads(self.get_argument('constants'))
    #         except:
    #             pass

    #         # Experimental: python mqtt client 不支持同一topic添加多个callback，尝试实现
    #         def single_callback(client, userdata, msg):

    #             # 0.1.19
    #             payload = json.loads(msg.payload)
    #             if "content" in payload:
    #                 message = payload["content"]
    #             else:
    #                 message = payload
    #             message.update(constants)

    #             # message = json.loads(msg.payload)["content"]
    #             # message.update(constants)

    #             result = self.service(srv_name, message)
    #             if result is not None:
    #                 # Decode input
    #                 self.mqtt.publish(pub_topic, json.dumps(
    #                     {'content': result}, ensure_ascii=False), qos)

    #         cbs = []
    #         if sub_topic in self.srv.gcbs:
    #             cbs = self.srv.gcbs[sub_topic] + [single_callback]
    #             print("Add callback at " + sub_topic)
    #         else:
    #             cbs = [single_callback]
    #         self.srv.gcbs[sub_topic] = cbs

    #         def on_subs_callback(client, userdata, msg):
    #             for cb in cbs:
    #                 cb(client, userdata, msg)

    #         self.mqtt.message_callback_add(sub_topic, on_subs_callback)
    #         # Sub input
    #         print("MQTT Service Subscribe: {0}, {1}, {2}, {3}, Added service: {4}".format(
    #             self._dev_id, op, sub_topic, pub_topic, srv_name))

    #         # Save
    #         flow_models_JSON = self.sql.query(
    #             Flow).filter_by(id=self.model['id']).first()
    #         flow_model = {"_dev_id": self.model['id'], "srv_name": srv_name,
    #                       "sub_topic": sub_topic, "pub_topic": pub_topic, "qos": qos}

    #         if flow_models_JSON is None:
    #             flow_models = [flow_model]
    #         else:
    #             flow_models = json.loads(flow_models_JSON.content)
    #             if flow_model in flow_models:
    #                 return
    #             else:
    #                 flow_models.append(flow_model)

    #         if flow_models_JSON is None:
    #             self.sql.add(
    #                 Flow(id=self.model['id'], content=json.dumps(flow_models)))
    #         else:
    #             flow_models_JSON.content = json.dumps(flow_models)
    #         self.sql.commit()
    #         print("Flow Added")

    #     elif (op == "remove"):
    #         print("MQTT Service Unsubscribe")
    #         flow_models_JSON = self.sql.query(
    #             Flow).filter_by(id=self.model['id']).first()
    #         if flow_models_JSON is not None:
    #             flow_models = json.loads(flow_models_JSON.content)
    #             for model in flow_models:
    #                 self.mqtt.unsubscribe(model['sub_topic'])
    #                 self.mqtt.message_callback_remove(model['sub_topic'])
    #                 # 0.1.19
    #                 if model['sub_topic'] in self.srv.gcbs:
    #                     print("Remove global callback array at " +
    #                           model['sub_topic'])
    #                     del self.srv.gcbs[model['sub_topic']]
    #                 flow_models.remove(model)
    #                 print("Flow Deleted: " + model['sub_topic'])
    #             flow_models_JSON.content = json.dumps(flow_models)
    #         self.sql.commit()

    # def deleteAllFlows(self):
    #     flows = self.sql.query(Flow).all()
    #     try:
    #         if len(flows) > 0:
    #             for fs in flows:
    #                 flowModels = json.loads(fs.content)
    #                 for f in flowModels:
    #                     self.mqtt.unsubscribe(f['sub_topic'])
    #                     self.mqtt.message_callback_remove(f['sub_topic'])
    #                     # 0.1.19
    #                     if f['sub_topic'] in self.srv.gcbs:
    #                         print("Remove global callback array at " +
    #                               f['sub_topic'])
    #                         del self.srv.gcbs[f['sub_topic']]
    #                 self.sql.delete(fs)
    #         self.sql.commit()
    #     except Exception as e:
    #         return "Failed to delete"
    #     return "OK"

    # def getAllFlows(self):
    #     try:
    #         res = self.sql.query(Flow).all()[0].content
    #         return json.dumps(res)
    #     except Exception as e:
    #         return []


class Ping(CustomHandler):
    def get(self):
        self.write("OK")

# # 读取/操作

# # GET: {srv-name}/property/{property-name}
# # POST: {srv-name}/action/{function-name}
# # POST & MQTT: {srv-name}/event/{event-name}

# 【弃用】
# class DevProperty(CustomHandler):
#     def initialize(self, dev, srv):
#         self.dev = dev
#         self.srv = srv

#     def post(self, key: str):
#         # self.write(self.dev.ReadProperty(key, content))
#         self.write(json.dumps({key: self.dev.resources[key]}))


# class DevService(CustomHandler):
#     def initialize(self, dev, srv):
#         self.dev = dev
#         self.srv = srv

#     def get(self, srv_name: str):
#         self.write(json.dumps(self.srv.selector(srv_name)))

#     def post(self, srv_name: str):
#         args = self.get_argument_dict()
#         self.write(json.dumps(self.dev.service(srv_name, args)))


class DevSelector(CustomHandler):
    def initialize(self, dev, srv):
        self.dev = dev
        self.srv = srv
        self.mqtt = srv.mqtt

    def post(self, func_name: str):
        args = self.get_argument_dict()
        self.write(json.dumps(self.dev.selector(func_name, args)))


# class DevEvent(CustomHandler):
#     def initialize(self, dev, srv):
#         self.dev = dev
#         self.srv = srv
#         self.mqtt = srv.mqtt

#     def post(self, event_name: str):
#         setup = int(self.get_argument('setup'))  # 0 = off, 1 = on
#         pub_topic = self.get_argument('pub_topic')
#         qos = 1
#         try:
#             qos = int(self.get_argument('qos'))
#         except:
#             pass

#         print("Event Subscribed: {0}, {1}".format(setup, pub_topic))

#         def on_event_callback(content):
#             if (setup > 0):
#                 print("Event auto-pubed: {0}, {1}".format(setup, pub_topic))
#                 self.mqtt.publish(pub_topic, json.dumps(
#                     {'content': content}, ensure_ascii=False), qos)

#         if not hasattr(self.srv.app, 'ecbs'):
#             print("ecb not initiated")
#             self.write("Error: ecb not initiated")
#         else:
#             self.srv.app.ecbs[event_name] = on_event_callback
#             self.write("OK")

# # MQTT 操作 (Flow)


# class DevMqttOp(CustomHandler):
#     def initialize(self, dev, srv):
#         self.dev = dev
#         self.srv = srv
#         self.mqtt = srv.mqtt

#     def post(self, srv_name: str):
#         self.dev.flow(srv_name=srv_name, **json_decode(self.request.body))
#         self.write("OK")

#     # delete all flows
#     def delete(self, op: str):
#         if op == "all":
#             self.write(self.dev.deleteAllFlows())

#     # get all flows
#     def get(self, op: str):
#         if op == "all":
#             res = self.dev.getAllFlows()
#             if len(res) == 0:
#                 res = '[]'

#             self.write(res)

# # Protocol 协议服务专用
# class DevProc(CustomHandler):
#     def initialize(self, dev, srv):
#         self.dev = dev
#         self.srv = srv

#     # Add new model
#     def post(self):
#         print(self.request.headers['Content-Type'])
#         model = self.sql.query(Entry).filter_by(id=self.get_argument('id')).first()

#         if model == None:
#             # Add
#             model = Entry(id=self.get_argument('id'), content=self.request.body.decode("utf-8"))
#             print("Device Added")
#             self.sql.add(model)
#         else:
#             # Update
#             model.content = self.request.body.decode("utf-8")
#             print("Device exists, update")
#         self.sql.commit()
#         self.set_status(200)
#         self.write('{0}'.format(model))

#     # Get all models
#     def get(self):
#         print("Get Devices")
#         model = self.sql.query(Entry).all()
#         # stop()
#         # model = [c.content for c in self.sql.query(Entry).all()]
#         self.set_status(200)
#         self.write("{0}".format(model))

# class DevProcID(CustomHandler):
#     def initialize(self, dev, srv):
#         self.dev = dev
#         self.srv = srv

#     # Delete model
#     def delete(self, id):
#         print("Delete Device - ID: "+ id)
#         model = self.sql.query(Entry).filter_by(id=id).first()
#         self.sql.delete(model)
#         self.sql.commit()
#         self.set_status(200)
#         self.write("{0}".format(model))

#     # Update model
#     def post(self, id):
#         print("Update Device - ID: "+ id)
#         model = self.sql.query(Entry).filter_by(id=id).first()
#         model.content = self.request.body.decode("utf-8")
#         self.sql.commit()
#         self.set_status(200)
#         self.write("{0}".format(model))

#     # Get model
#     def get(self, id: str):
#         print("Get Entry - ID: "+ id)
#         model = self.sql.query(Entry).filter_by(id=id).first()
#         self.set_status(200)
#         self.write("{0}".format(model))
