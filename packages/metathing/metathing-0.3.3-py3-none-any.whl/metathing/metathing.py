# Copyright: 北京物元数界科技有限公司
# Author: 邵芒
# Contact: 微信 stormx

from metathing.service import Service
from metathing.logger import logger
import socket, time, os
import struct, json, inspect, yaml
from pdb import set_trace as stop

MCAST_GRP = '239.1.2.3'
MCAST_PORT = 34567
RECV_MCAST_PORT = 34568

class MetaThing():
    def __init__(self, config: object, srv_name: str):
        self.srv = Service(config, srv_name)
        self.addr = None

    def Bind(self, app:object):
        self.srv.mqtt.connect()
        self.srv.Bind(app)
        app.LoadModel()

    def Run(self):
        self.srv.http.Run()
        
    def OpenIPBroadcast(self):
        import threading
        t = threading.Thread(target=MetaThing.MTNodeIPSend)
        logger.info('[Auth]: Starting IP broadcast thread...')
        t.start()

    # 首字符为大写或下划线的函数名将被忽略
    def MTGenAdapterModel(self, app_path):
        # Get apapter model from graph
        query = '''{
            result(func: eq(srv_id, "{srv_id}")) @filter(type(AdapterSchema))
            {
                uid
                adapteract {
                    act_tag is_global
                    srv_input { var_tag dtype }
                    srv_output { var_tag dtype }
                }
                adapterevt {
                    evt_tag is_global
                    srv_output { var_tag dtype }
                }
                device_init_config {
                    var_tag dtype default
                }
                init_config {
                    var_tag dtype default
                }
            }}'''
        query = query.replace('{srv_id}', self.srv.srv_name)
        
        def check_built_in(name):
            return name[0] != '_' and name[0].islower() and name != "ping" and name != "selector" and name != "release"
        predicate = lambda x,y: check_built_in(x) and callable(y)
        
        # App
        app_fns = [(name, member) for name, member in inspect.getmembers(self.srv.app) if predicate(name, member) ]
        
        # Dev
        dev_fns = [(name, member) for name, member in inspect.getmembers(self.srv.app.Dev) if predicate(name, member)]
        
        def fn_exists_in_model(item, is_global):
            is_event = 'evt_tag' in item
            fn_name = item['evt_tag'] if is_event else item['act_tag']
            for name, fn in app_fns if is_global else dev_fns:
                if name == fn_name:
                    return True
            return False
        
        def model_contains_cfg(var_name, is_global):
            if len(am) == 0:
                return False
            if is_global == True and 'init_config' in am:
                for item in am['init_config']:
                    if item['var_tag'] == var_name:
                        return True
            elif is_global == False and 'device_init_config' in am:
                for item in am['device_init_config']:
                    if item['var_tag'] == var_name:
                        return True
        
        def model_contains_fn(fn_name, is_event, is_global):
            if len(am) == 0:
                return False
            field = 'adapterevt' if is_event else 'adapteract'
            if not field in am:
                return False
            
            for item in am[field]:
                if item['evt_tag' if is_event else 'act_tag'] == fn_name and item['is_global'] == is_global:
                    return True
            return False
        
        
        # Append missing items to adapter model
        def gen_adapter_var(item):
            return {
                "srv_id": self.srv.srv_name,
                "var_tag": item['var_name'],
                "name": item['name'],
                "name@zh": item['name@zh'] if 'name@zh' in item else item['name'],
                "dtype": item['dtype'],
                "default": item['default'] if 'default' in item else None,
                "dgraph.type": "AdapterVar",
            }
            
        def gen_adapter_fn(fn_name, item, is_act, is_global):
            res = {
                "srv_id": self.srv.srv_name,
                "name": item['name'],
                "name@zh": item['name@zh'] if 'name@zh' in item else item['name'],
                "topic": f"/{self.srv.srv_name}/{fn_name}" if is_global else f"/{self.srv.srv_name}/devices/{{dev_id}}/selectors/{fn_name}",
                "is_global": is_global,
                "description": item['description'] if 'description' in item else None,
                "description@zh": item['description@zh'] if 'description@zh' in item else item['description'] if 'description' in item else None,
                "dgraph.type": "AdapterAct" if is_act else "AdapterEvt",
            }
            if is_act:
                res['act_tag'] = fn[0]
            else:
                res['evt_tag'] = fn[0]
            return res
        
        missing_model_fields = {
            "app_config": [],
            "dev_config": [],
            "act": [],
            "evt": [],
        }
        full_model_fields = {
            "app_config": [],
            "dev_config": [],
            "act": [],
            "evt": [],
        }
        
        res = self.srv.mqtt.publish_request("/graph/devices/01/selectors/query", json.dumps({"data":{"query":query}}), qos=1, timeout=5)
        if res is None:
            logger.error('[MTGenAdapterModel]: MQTT request timeout, please check core services')
            return
        else:
            am = json.loads(res)['result']
            if len(am) > 0:
                am = am[0]
                message = [
                    f"!-= Adapter model exists =-",
                    f"UID: {am['uid']}",
                ]
                def print_model_items(_items, _message, is_global):
                    for item in _items:
                        fn_name = item['act_tag'] if 'act_tag' in item else item['evt_tag']
                        _message.append(f"Fn: [{fn_name}]")
                        if not fn_exists_in_model(item, is_global):
                            _message.append(f"@ {fn_name} not found!")
                        
                        if 'srv_input' in item:
                            _message.append(f":In: {len(item['srv_input'])}")
                            for idx, i in enumerate(item['srv_input']):
                                _message.append(f":In[{idx}]: {i['var_tag']} ({i['dtype']})")
                        if 'srv_output' in item:
                            for idx, i in enumerate(item['srv_output']):
                                message.append(f":Out[{idx}]: {i['var_tag']} ({i['dtype']})")
                message.append("")
                if 'adapteract' in am:
                    items = [item for item in am['adapteract'] if item['is_global'] == True]
                    if len(items) > 0:
                        message.append("!- Application: Action -")
                        print_model_items(items, message, True)
                        message.append("")
                if 'adapterevt' in am:
                    items = [item for item in am['adapterevt'] if item['is_global'] == True]
                    if len(items) > 0:
                        message.append("!- Application: Event -")
                        print_model_items(items, message, True)
                        message.append("")
                if 'adapteract' in am:
                    items = [item for item in am['adapteract'] if item['is_global'] == False]
                    if len(items) > 0:
                        message.append("!- Device: Action -")
                        print_model_items(items, message, False)
                        message.append("")
                if 'adapterevt' in am:
                    items = [item for item in am['adapterevt'] if item['is_global'] == False]
                    if len(items) > 0:
                        message.append("!- Device: Event -")
                        print_model_items(items, message, False)
                        message.append("")
                self.srv.app._print_frame(message)
            else:
                message = [
                    f"!-= Creating new adapter model =-",
                ]
                self.srv.app._print_frame(message)
        
        def get_yaml(title, lines, do_print=True):
            if lines is None:
                return None
            try:
                return yaml.load(lines, yaml.FullLoader)
            except Exception as e:
                logger.error(f'[{title}]: Cannot load lines, reason: {e}')
                return None

        # Get service info from docs
        # Main
        import __main__
        
        # 注意：当无法提取__main__.__doc__时，将默认已进行了cython编译，无法提取注释。将自动使用 app 目录下 {srv_id}.schema 作为适配模型。
        info = get_yaml('Service Info', __main__.__doc__)
       
        if info is None:
            message = [f"@-= Main.py head comment cannot be found, assume script is compiled =-"]
            self.srv.app._print_frame(message)
    
            fn = f'{app_path}/{self.srv.srv_name}.schema'
            # Load yaml, create adapter model only if UID not exist
            if isinstance(am, list) and len(am) == 0 and os.path.exists(fn):
                with open(fn, 'r') as f:
                    model = yaml.load(f, yaml.FullLoader)
                    self.srv.app._print_frame(['!-= Upserting Model -=']+yaml.dump(model, sort_keys=False, allow_unicode=True).split('\n'))
                    # Write to graphDB
                    res = self.srv.mqtt.publish_request("/graph/devices/01/selectors/mutate", json.dumps({"data":model}), qos=1, timeout=5)
                    if res is not None:
                        self.srv.app._print_frame(['!-= Model successfully upserted! =-'])
            else:
                self.srv.app._print_frame(['!-= Adapter model exists or schema file is missing! =-'])
            return

        message = [
            f"!-= Service Info =-",
            f":Name: {info['name']}",
            f":Desc: {info['description']}",
            f":Icon: {info['icon'] if 'icon' in info else ''}",
        ]
        self.srv.app._print_frame(message)
        
        # Red -> Fn not exists in model
        def scan_fn_info(fn_config, message, is_event, is_global):
            exists = model_contains_fn(fn[0], is_event, is_global)
            if fn_config is not None and 'name' in fn_config:
                tmp_model_field = gen_adapter_fn(fn[0], fn_config, not is_event, is_global)
                message = message + [
                    f"{'@[未注册] ' if not exists else ''}Fn: {fn[0]}",
                    f":  Name: {fn_config['name']}",
                    f":  Desc: {fn_config['description'] if 'description' in fn_config else ''}",
                ]
                if 'input' in fn_config:
                    if tmp_model_field is not None:
                        tmp_model_field['srv_input'] = []
                    message = message + [f':  Input:']
                    for item in fn_config['input']:
                        message = message + [
                            f":    {item['var_name']}.Name: {item['name']}",
                            f":    {item['var_name']}.Type: {item['dtype']}",
                            f":    {item['var_name']}.Desc: {item['description'] if 'description' in item else ''}",
                            ""
                        ]
                        if tmp_model_field is not None and 'srv_input' in tmp_model_field:
                            tmp_model_field['srv_input'].append(gen_adapter_var(item))
                if 'output' in fn_config:
                    message = message + [f':  Output:']
                    if tmp_model_field is not None:
                        tmp_model_field['srv_output'] = []
                    for item in fn_config['output']:
                        message = message + [
                            f":    {item['var_name']}.Name: {item['name']}",
                            f":    {item['var_name']}.Type: {item['dtype']}",
                            f":    {item['var_name']}.Desc: {item['description'] if 'description' in item else ''}",
                            ""
                        ]
                        if tmp_model_field is not None and 'srv_output' in tmp_model_field:
                            tmp_model_field['srv_output'].append(gen_adapter_var(item))
                if tmp_model_field is not None:
                    if not exists:
                        missing_model_fields['act' if not is_event else 'evt'].append(tmp_model_field)
                    full_model_fields['act' if not is_event else 'evt'].append(tmp_model_field)
            else:
                message = message + [
                    f"{'@[未注释] ' if not exists else ''}Fn: {fn[0]} (No info)",
                ]
            return message
        
        # App
        app_config = get_yaml('App Info', self.srv.app.__doc__)
        if app_config is not None and 'config' in app_config:
            message = ['!- Application Configs -']
            for item in app_config['config']:
                message = message + [
                    f"{item['var_name']}.Name: {item['name']} ",
                    f"{item['var_name']}.Type: {item['dtype']}",
                    f"{item['var_name']}.default: {item['default'] if 'default' in item else ''}",
                    ""
                ]
                if not model_contains_cfg(item['var_name'], True):
                    missing_model_fields['app_config'].append(gen_adapter_var(item))
                full_model_fields['app_config'].append(gen_adapter_var(item))
            self.srv.app._print_frame(message)
            
        if len(app_fns) > 0:
            message = [
                f"!-= Application Action =-",
            ]
            for fn in app_fns:
                fn_config = get_yaml('Action Info', fn[1].__doc__)
                if not hasattr(fn[1], "__is_event__"):
                    message = scan_fn_info(fn_config, message, False, True)
            message.append("!-= Application Event =-")
            for fn in app_fns:
                fn_config = get_yaml('Event Info', fn[1].__doc__)
                if hasattr(fn[1], "__is_event__"):
                    fn_config = get_yaml('Event Info', fn[1].__is_event__.__doc__)
                    message = scan_fn_info(fn_config, message, True, True)
            self.srv.app._print_frame(message)
        
        dev_config = get_yaml('Device Info', self.srv.app.Dev.__doc__)
        if dev_config is not None and 'config' in dev_config:
            message = ['!- Device Configs -']
            for item in dev_config['config']:
                message = message + [
                    f"{item['var_name']}.Name: {item['name']}",
                    f"{item['var_name']}.Type: {item['dtype']}",
                    f"{item['var_name']}.Default: {item['default'] if 'default' in item else ''}",
                    ""
                ]
                if not model_contains_cfg(item['var_name'], False):
                    missing_model_fields['dev_config'].append(gen_adapter_var(item))
                full_model_fields['dev_config'].append(gen_adapter_var(item))
            self.srv.app._print_frame(message)
            
        if len(dev_fns) > 0:
            message = [
                f"!-= Device Action =-",
            ]
            for fn in dev_fns:
                fn_config = get_yaml('Action Info', fn[1].__doc__)
                if not hasattr(fn[1], "__is_event__"):
                    message = scan_fn_info(fn_config, message, False, False)
            message.append("!-= Device Event =-")
            for fn in dev_fns:
                fn_config = get_yaml('Event Info', fn[1].__doc__)
                if hasattr(fn[1], "__is_event__"):
                    fn_config = get_yaml('Event Info', fn[1].__is_event__.__doc__)
                    message = scan_fn_info(fn_config, message, True, False)
            self.srv.app._print_frame(message)
        
        # Writing adapter model
        # If no adapter model, create new one, else inherit UID
        def load_gdb_model(is_for_mutation, model_fields):
            model = {}
            if is_for_mutation and am is not None and not isinstance(am, list):
                model['uid'] = am['uid']
            else:
                model['dgraph.type'] = 'AdapterSchema'
                model['name'] = info['name']
                model['name@zh'] = info['name@zh'] if 'name@zh' in info else info['name']
                model['description'] = info['description']
                model['icon'] = info['icon'] if 'icon' in info else ''
                model['description@zh'] = info['description@zh'] if 'description@zh' in info else info['description']
                model['srv_id'] = self.srv.srv_name
            
            # Import configs
            model['init_config'] = model_fields['app_config']
            model['device_init_config'] = model_fields['dev_config']
            model['adapteract'] = model_fields['act']
            model['adapterevt'] = model_fields['evt']
            return model
            
        model = load_gdb_model(True, missing_model_fields)
        self.srv.app._print_frame(['!-= Upserting Model -=']+yaml.dump(model, sort_keys=False, allow_unicode=True).split('\n'))
        
        full_model = load_gdb_model(False, full_model_fields)
        # Store full model locally in case of cython compilation
        with open(f'{app_path}/{self.srv.srv_name}.schema', 'w') as f:
            f.write(yaml.dump(full_model, sort_keys=False, allow_unicode=True))
        
        # Write to graphDB
        res = self.srv.mqtt.publish_request("/graph/devices/01/selectors/mutate", json.dumps({"data":model}), qos=1, timeout=5)
        if res is not None:
            self.srv.app._print_frame(['!-= Model successfully upserted! =-'])
        
    @staticmethod
    def PipDownload(lib_list):
        import subprocess, sys
        for lib in lib_list:
            # Check lib exists
            try:
                __import__(lib[0])
                continue
            except:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib[1]])
        
    @staticmethod
    def KillProcessWithSameIpAndPort(ip, port):
        import psutil
        current_pid = psutil.Process().pid 
        for conn in psutil.net_connections():
            if conn.laddr.ip == ip and conn.laddr.port == port and conn.pid != current_pid:
                pid = conn.pid
                psutil.Process(pid).kill()
                logger.warning(f"Killed conflicted process with pid {pid}")
        
    @staticmethod
    def MTNodeIPRequest():
        req_msg = 'MTNode_IP_REQUEST'
        time.sleep(5)
        
        # Check connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_recv.bind(('', RECV_MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock_recv.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock_recv.settimeout(5)
        while True:
            sock.sendto(req_msg.encode(), (MCAST_GRP, MCAST_PORT))
            try:
                logger.info('Requesting MTNode IP...')
                data, address = sock_recv.recvfrom(1024)
                data = data.decode()
                logger.info(f'Success: {data}')
                sock.close()
                sock_recv.close()
                return data
            except:
                logger.info('Timeout, retrying...')
        
    @staticmethod        
    def MTNodeIPSend():
        ready = False
        while not ready:  
            # attempt to reconnect, otherwise sleep for 2 seconds  
            try:  
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(('', MCAST_PORT))
                mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                sock_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sock_sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
                csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                csock.connect(('8.8.8.8', 80))
                (addr, port) = csock.getsockname()
                csock.close()
                ready = True
            except:  
                time.sleep(2)  
                
        while True:
            data, address = sock.recvfrom(1024)
            if data == b'MTNode_IP_REQUEST':
                logger.info(f'Received request from: {address}')
                logger.info(f'Sending my address: {addr}')
                sock_sender.sendto(addr.encode(), (MCAST_GRP, RECV_MCAST_PORT))

# if __name__ == '__main__':
#     # Open a thread to run MetaThing.MTNodeIPSend()
#     import threading
#     t = threading.Thread(target=MetaThing.MTNodeIPSend)
#     t.start()
    
#     MetaThing.MTNodeIPRequest()     