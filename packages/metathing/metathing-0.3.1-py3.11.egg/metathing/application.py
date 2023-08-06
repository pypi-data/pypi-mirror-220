# Copyright: 北京物元数界科技有限公司
# Author: 邵芒
# Contact: 微信 stormx

import json
from metathing.logger import logger
import inspect
from functools import partial
from pdb import set_trace as stop
import sys
import unicodedata, textwrap

class Application():
    def __init__(self):
        self.srv = None
        self.Dev = None
        self.event_sender = {}
        self.devs = {}

    def AddDev(self, model):
        if self.Dev is None:
            raise Exception("Device model not defined!")
        dev_id = model['dev_id']
        if 'init_config' in model:
            config = model['init_config']
        config['dev_id'] = dev_id
        self.devs[dev_id] = self.Dev(self.srv, config)
        
    def UpdateDev(self, model):
        self.AddDev(model)

    def DeleteDev(self, id):
        if (id in self.devs):
            print("Releasing: "+id)
            self.devs[id].release()
            del self.devs[id]

    def DevsInfo(self):
        devs_info = {}
        for _dev_id, dev in self.devs.items():
            devs_info[_dev_id] = dev.model
        return devs_info
        
    def Event(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            # Get function name
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
            logger.error("Action not found [{0}]".format(fn_name))
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
                for k,v in res.items():
                    message.append(f"{k}: {v}")
                if hasattr(msg, 'properties') and hasattr(msg.properties, 'ResponseTopic'):
                    message.append(f"- ResponseTopic -")
                    message.append(f"{msg.properties.ResponseTopic}")
                    self.srv.mqtt.publish(msg.properties.ResponseTopic, json.dumps(res))
                self._print_frame(message)
            except Exception as e:
                print(e)
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
    
    def LoadModel(self, gdb_topic = "/auth/query_adapter_config"):
        try:
            res = self.srv.mqtt.publish_request(gdb_topic, json.dumps({'data': {'srv_id': self.srv.srv_name}}))
            self._processing_model(res)
            return True
        except Exception as e:
            logger.error("Load model error: {0}".format(e))
            print(e)
            return None
              
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
    
    def _processing_model(self, res: str):
        try:
            if res == 'null' or res is None:
                self._print_frame(["* Service has not been registered in MTNode *"])
                return None
            model = json.loads(res)
            self.model = model
            message = [
                f"-= {self.srv.srv_name} =-",
                f"UID: {model['uid']}",
            ]
            
            if 'init_config' in model:
                message.append("")
                message.append(f"- Config -")
                for k, v in model['init_config'].items():
                    message.append(f"{k}: {v}")
                    setattr(self, k, v)
                    message.append("")
                    
            if 'device_model' in model and len(model['device_model']) > 0:
                for device in model['device_model']:
                    self.AddDev(device)
                    message.append(f"Device: [{device['dev_id']}]")
                    if 'init_config' in device:
                        for k, v in device['init_config'].items():
                            message.append(f"{k}: {v}")
                    message.append("")
            
            message.append('- Registered Actions and Events -')
            
            name_map = {
                'srv_act': 'Global Actions',
                'srv_evt': 'Global Events',
                'dev_act': 'Device Actions',
                'dev_evt': 'Device Events',
            }
            for key in ['srv_act', 'srv_evt', 'dev_act', 'dev_evt']:                
                if key in model and len(model[key]) > 0:
                    message.append("")
                    message.append(f"{name_map[key]}: [{len(model[key])}] items")
                    for item in model[key]:
                        if key == 'srv_act': self.BindAction(item) 
                        if key == 'srv_evt': self.BindEvent(item)
                        if key == 'dev_act': 
                            if not 'dev_id' in item:
                                logger.error("Device ID miss-linked （设备ID绑定错误，可能是因为适配服务被改动而实例服务未更新）")
                            dev_id = item['dev_id']
                            if not dev_id in self.devs:
                                logger.error("Device not found [{0}]".format(dev_id))
                            self.devs[dev_id].BindAction(item)
                        if key == 'dev_evt':
                            if not 'dev_id' in item:
                                logger.error("Device ID miss-linked （设备ID绑定错误，可能是因为适配服务被改动而实例服务未更新）")
                            dev_id = item['dev_id']
                            if not dev_id in self.devs:
                                logger.error("Device not found [{0}]".format(dev_id))
                            self.devs[dev_id].BindEvent(item)
                        message.append(f"{item['tag']}({item['topic']}): In[{len(item['srv_input']) if 'srv_input' in item and item['srv_input'] else 0 }] Out[{len(item['srv_output']) if 'srv_output' in item and item['srv_output'] else 0 }]")
            self._print_frame(message)
        except Exception as e:
            logger.error("Load model error: {0}".format(e))
            print(e)
            return None
              
    @staticmethod
    def _print_frame(content, center_align = False):
        def count_fullwidth_chars(text):
            count = 0
            for char in text:
                if unicodedata.east_asian_width(char) != 'Na':
                    count += 1
            return count

        def len_plus(text):
            return len(text) + count_fullwidth_chars(text)

        frame_width = len_plus(max(content, key=len_plus)) + 4
        frame = '+' + '-' * (frame_width) + '+'
        logger.info(frame)
        for _line in content:
            line_len = len(_line) + count_fullwidth_chars(_line)
            new_lines = textwrap.wrap(_line, width=80)
            
            for line in new_lines:
                line_len = len(line) + count_fullwidth_chars(line)
                spaces_before = int((frame_width - line_len) / 2)
                spaces_after = frame_width - line_len - spaces_before
                def add_frame(line):
                    if center_align:
                        string = '|' + ' ' * spaces_before + line + ' ' * spaces_after + '|'
                    else:
                        string = '|  ' + line + ' ' * (spaces_before + spaces_after - 2) + '|'
                    return string
                if line != '':
                    if line[0] == '!':
                        line = line.replace('!', '', 1) + ' '
                        logger.warning(add_frame(line))
                    elif line[0] == '@':
                        line = line.replace('@', '', 1) + ' '
                        logger.error(add_frame(line))
                    elif line[0] == ':':
                        line = line.replace(':', '', 1) + ' '
                        logger.green(add_frame(line))
                    else:
                        logger.info(add_frame(line))
                else:
                    logger.info(add_frame(line))
        logger.info(frame)
              
    # Customized functions
    def ping(self):
        return "OK"
          
    def release(self):
        return {}