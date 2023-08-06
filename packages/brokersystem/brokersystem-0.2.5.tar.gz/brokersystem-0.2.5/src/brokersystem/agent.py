import threading
import json, traceback, time, importlib, sys, io
import os, glob, importlib
from functools import partial
import inspect
import pandas as pd
import requests
from logzero import logger
from PIL import Image as PILImage




class ValueTemplate:
    def __init__(self, unit=None):
        self.type = self.__class__.__name__.lower()
        self.unit = unit
        self.constraint_dict = {}
        self.item_type = None
    
    def set_constraint(self, key, value):
        if value is not None:
            self.constraint_dict[key] = value
    
    @property
    def format_dict(self):
        format = {"@type": self.type, "@unit": self.unit}
        if self.item_type == "input":
            format.update({"@necessity": "required", "@constraints": self.constraint_dict})
        if self.item_type == "output":
            format.update({})
        return format

    def cast(self, value):
        return value

    def format_for_output(self, value, uploader):
        format_dict = {"@type": self.type, "@unit": self.unit}
        return value, format_dict
    
    def set_item_type(self, item_type):
        self.item_type = item_type
    
    @classmethod
    def guess_from_value(self, value, unit_callback_func=None, key=None):
        unit = None
        if isinstance(value, (int, float)):
            if unit_callback_func is not None:
                unit = unit_callback_func(key)
            return Number(value, unit=unit)
        if isinstance(value, (str)):
            return String(value)

        if isinstance(value, pd.DataFrame) or (isinstance(value, list) and all([isinstance(x, dict) for x in value])) or (isinstance(value, dict) and all([isinstance(x, list) for x in value.values()])):
            if not isinstance(value, pd.DataFrame):
                value = pd.DataFrame(value)
            unit_dict = {}
            for column in value.columns:
                unit_dict[column] = unit_callback_func(column)
            option_dict = {}
            if len(value.columns) >= 2:
                option_dict["graph"] = {"x": value.columns[0], "y": value.columns[1]}
            return Table(unit_dict=unit_dict, **option_dict)
        
        if isinstance(value, (list)):
            return Choice()

        assert False, f"Cannot find a matching value template... {value}:{type(value)}"
    
    @classmethod
    def from_dict(cls, format_dict, unit_dict):
        option_dict = {}
        if format_dict["@type"] == "number":
            template = Number()
        if format_dict["@type"] == "string":
            template = String()
        if format_dict["@type"] == "choice":
            template = Choice(format_dict["@constraints"]["choices"])
        if format_dict["@type"] == "table":
            unit_dict = {key: unit_dict[key] for key in format_dict["@table"]}
            if "@repr" in format_dict and format_dict["@repr"]["type"] == "graph":
                option_dict["graph"] = {"x": format_dict["@repr"]["key_x"], "y": format_dict["@repr"]["key_y"]}
            template = Table(unit_dict=unit_dict, **option_dict)
        if "@constraints" in format_dict:
            for key, value in format_dict["@constraints"].items():
                template.set_constraint(key, value)
        if "@unit" in format_dict:
            template.unit = format_dict["@unit"]
        
        return template
            

class Number(ValueTemplate):
    def __init__(self, value=None, unit=None, min=None, max=None):
        super().__init__(unit)
        self.set_constraint("default", value)
        self.set_constraint("min", min)
        self.set_constraint("max", max)
    
    def cast(self, value):
        try:
            value = int(value)
        except:
            value = float(value)
        assert not ("min" in self.constraint_dict and value < self.constraint_dict["min"])
        assert not ("max" in self.constraint_dict and value > self.constraint_dict["max"])
        return value

class Range(ValueTemplate):
    def __init__(self, range_min=None, range_max=None, unit=None):
        super().__init__(unit)
        self.set_constraint("default", {"min": range_min, "max": range_max})

class String(ValueTemplate):
    def __init__(self, string=None):
        super().__init__()
        self.set_constraint("default", string)

class File(ValueTemplate):
    def __init__(self, file_type=None):
        super().__init__()
        if file_type in ["png", "jpeg", "gif"]:
            self.type = "image"
        self.file_type = file_type
        self.set_constraint("file_type", file_type)

    def format_for_output(self, value, uploader):
        format_dict = self.format_dict
        if isinstance(value, str) and self.type == "image":
            if self.file_type in ["png", "jpeg"]:
                img = PILImage.open(value)
                output = io.BytesIO()
                img.save(output, format=self.file_type)
                binary_data = output.getvalue()
            if self.file_type == "gif":
                with open(value, "rb") as f:
                    binary_data = f.read()
            response = uploader(self.file_type, binary_data)
            print(response)
            assert "file_id" in response
            value = response["file_id"]
        elif isinstance(value, str) and self.type == "file":
            with open(value, "rb") as f:
                binary_data = f.read()
            response = uploader(self.file_type, binary_data)
            print(response)
            assert "file_id" in response
            value = response["file_id"]
        else:
            raise 
        
        return value, format_dict

class Choice(ValueTemplate):
    def __init__(self, choices: list, unit=None):
        super().__init__(unit)
        self.set_constraint("choices", choices)

    def cast(self, value):
        try:
            value = int(value)
        except:
            pass
        try:
            value = float(value)
        except:
            pass
        assert value in self.constraint_dict["choices"]
        return value

class Table(ValueTemplate):
    def __init__(self, unit_dict:dict, graph:dict=None):
        super().__init__(unit=None)
        self.unit_dict = unit_dict.copy()
        self.graph = graph

    def cast(self, value):
        return value

    @property
    def format_dict(self):
        format_dict = super().format_dict
        format_dict["@table"] = list(self.unit_dict.keys())
        format_dict["_unit_dict"] = self.unit_dict
        if self.graph is not None:
            format_dict["@repr"] = {"type": "graph", "key_x": self.graph["x"], "key_y": self.graph["y"]}
        return format_dict

    def format_for_output(self, value, uploader):
        format_dict = self.format_dict
        if isinstance(value, pd.DataFrame):
            value = value.to_dict(orient="list")
        elif (isinstance(value, list) and all([isinstance(x, dict) for x in value])) or (isinstance(value, dict) and all([isinstance(x, list) for x in value.values()])):
            value = pd.DataFrame(value).to_dict(orient="list") 
        else:
            raise Exception("The return value for table should be given by a list of dict, a dict of list or pandas DataFrame")
        
        keys = list(value.keys())
        if self.graph is None and len(keys) >= 2:
            format_dict["@repr"] = {"type": "graph", "key_x": keys[0], "key_y": keys[1]}

        return value, format_dict
            

class TemplateContainer:
    def __init__(self, item_type):
        self._container_dict = {}
        self._value_keys = []
        self._table_keys = []
        self._item_type = item_type

    def __setattr__(self, key: str, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
            return
        if not isinstance(value, ValueTemplate):
            logger.error(f"You can only set ValueTemplate object(such as Number or Table) for input, condition and output: {key} ({type(value)})")
            return
        self._container_dict[key] = value
        if isinstance(value, Table):
            if key not in self._table_keys:
                self._table_keys.append(key)
        elif key not in self._value_keys:
            self._value_keys.append(key)
        value.set_item_type(self._item_type)
    
    def _get_template(self):
        if self._item_type == "input":
            format_keys = ["@type", "@unit", "@necessity", "@constraints"]
        if self._item_type == "output":
            format_keys = ["@type", "@unit", "@repr"]
        if self._item_type == "condition":
            format_keys = ["@type", "@unit", "@value"]
        template_dict = {fkey: {} for fkey in format_keys}

        template_dict["@keys"] = self._value_keys + self._table_keys
        if len(self._value_keys) > 0:
            template_dict["@value"] = self._value_keys.copy()

        if len(self._table_keys) > 0:
            template_dict["@table"] = {} # will be given by Table instance

       
        for key, template in self._container_dict.items():
            for fkey, fvalue in template.format_dict.items():
                if fkey == "_unit_dict":
                    for k, v in fvalue.items():
                        assert k not in template_dict["@unit"] and k not in template_dict["@type"], f"Duplicated key error: {k}"
                        template_dict["@unit"][k] = v
                        template_dict["@type"][k] = "number"
                else:
                    assert key not in template_dict[fkey], f"Duplicated key error: {key}"
                    template_dict[fkey][key] = fvalue
        return template_dict
    
    def _load(self, config_dict):
        for key in config_dict["@keys"]:
            format_dict = {prop_key: config_dict[prop_key][key] for prop_key in config_dict.keys() if prop_key.startswith("@") and isinstance(config_dict[prop_key], dict) and key in config_dict[prop_key]}
            setattr(self, key, ValueTemplate.from_dict(format_dict, config_dict["@unit"]))
    
    def __contains__(self, key):
        return key in self._container_dict
    
    def __getitem__(self, key):
        return self._container_dict[key]

class ValueContainer:
    def __init__(self, value_dict):
        self._container_dict = value_dict.copy()

    def __getattr__(self, key: str):
        if key.startswith("_"):
            return super().__getattr__(key)
        return self._container_dict[key]
    
    def __getitem__(self, key: str):
        return self._container_dict[key]


class AgentInterface:
    def __init__(self):
        self.secret_token = ""
        self.name = None
        self.charge = 10000
        self.convention = ""
        self.description = ""
        self.input = TemplateContainer("input")
        self.condition = TemplateContainer("condition")
        self.output = TemplateContainer("output")
    
    def prepare(self, func_dict):
        self.func_dict = func_dict.copy()
        if "make_config" not in self.func_dict and (self.secret_token == "" or self.name == None):
            logger.error("Secret_token and name should be specified.")
            return
        if "job_func" not in self.func_dict:
            logger.error("job execution function is required: Prepare a decorated function with @job_func.")
            return
        self.make_config()

    def make_config(self, for_registration=False):
        if "make_config" in self.func_dict:
            self.func_dict["make_config"]()
            if self.name is None:
                logger.error("Agent's name should be set in config function")
        config_dict = {}
        for item_type in ["input", "condition", "output"]:
            config_dict[item_type] = getattr(getattr(self, item_type), "_get_template")()
        
        config_dict["charge"] = self.charge
        if for_registration:
            config_dict["module_version"] = __version__ if "__version__" in globals() else "-1.0.0"
            config_dict["convention"] = self.convention
            config_dict["description"] = self.description

        return config_dict
    
    def has_func(self, func_name):
        return func_name in self.func_dict
    
    def validate(self, input_dict):
        template_dict = self.input._get_template()
        msg = "ok"
        for key in template_dict["@keys"]:
            if key in input_dict:
                try:
                    value = self.input[key].cast(input_dict[key])
                    template_dict[key] = value
                except [AssertionError, TypeError]:
                    msg = "need_revision"
        return msg, template_dict

    def cast(self, key, input_value):
        if key not in self.input:
            logger.error(f"{key} is not registered as input.")
            raise Exception
        return self.input[key].cast(input_value)
    
    def format_for_output(self, result_dict, uploader):
        output_dict = {"@unit": {}, "@type": {}, "@option": {}, "@repr": {}, "@keys": []}

        for key, value in result_dict.items():
            if key not in self.output:
                continue
            output_value, format_dict = self.output[key].format_for_output(value, uploader)
            if output_value is None:
                continue
            output_dict[key] = output_value
            output_dict["@keys"].append(key)
            ### manage type specific properties 
            if format_dict["@type"] == "table":
                if "@table" not in output_dict:
                    output_dict["@table"] = {}
                table_keys = list(format_dict["_unit_dict"].keys())
                output_dict["@unit"].update(format_dict["_unit_dict"])
                output_dict["@type"].update({k: "number" for k in table_keys})

            elif format_dict["@type"] in ["image", "file"]:
                if "@file" not in output_dict:
                    output_dict["@file"] = {}
            else:
                if "@value" not in output_dict:
                    output_dict["@value"] = []
                output_dict["@value"].append(key)

            for fk, fv in format_dict.items():
                if not fk.startswith("_"):
                    output_dict[fk][key] = fv
        # remove empty property keys
        
        return output_dict

class DummyJob:
    _to_show_i_am_job_class = True
    def __init__(self, request_params=None, config=None):
        class DummyAgentInterface:
            def __init__(self):
                self.secret_token = config["secret_token"]
        class DummyAgent:
            def __init__(self):
                if config is not None:
                    self.broker_url = config["broker_url"]
                    self.interface = DummyAgentInterface()
                
        self._agent = DummyAgent()

    def report(self, msg=None, progress=None, result=None):
        logger.info(f"[DUMMY JOB] REPORT: {msg}, {progress}, {result}")

    def __getitem__(self, key):
        return 0
    
    def __contains__(self, key):
        return True

class Job:
    _to_show_i_am_job_class = True
    def __init__(self, agent, negotiation_id, request):
        self._agent = agent
        self._negotiation_id = negotiation_id
        self._request = request
        self._result_dict = {}
        self._status = "init"
        self.id = negotiation_id
    
    def report(self, msg=None, progress=None, result=None):
        payload =  {"negotiation_id": self._negotiation_id, "status": self._status}
        if msg is not None:
            payload["msg"] = msg
        if progress is not None:
            payload["progress"] = progress
        if result is not None:
            assert isinstance(result, dict), "Result should be given as a dict: {result_key: result_value}"
            self._result_dict.update(result)
            payload["result"] = self._agent.interface.format_for_output(self._result_dict, self._agent.upload)

        self._agent.post("report", payload)

    def msg(self, msg):
        self.report(msg=msg)
    
    def progress(self, progress, msg=None):
        self.report(progress=progress, msg=msg)
    
    def periodic_report(self, estimated_time=None, interval=2, callback_func=None, **kwargs):
        if "start_time" not in kwargs:
            kwargs["start_time"] = time.time()
        if self._status not in ["done", "error"]:
            msg = None
            if callback_func is not None:
                kwargs["callback_func"] = callback_func
                msg = callback_func(self, **kwargs)
            if estimated_time is not None:
                kwargs["estimated_time"] = estimated_time
                self.progress((time.time()-kwargs["start_time"])/estimated_time, msg=msg)
            elif msg is not None:
                self.msg(msg)
            timer = threading.Timer(interval, self.periodic_report, kwargs=kwargs)
            timer.daemon = True
            timer.start()
        
    def __getitem__(self, key):
        return self._agent.interface.cast(key, self._request[key])
    
    def __contains__(self, key):
        return key in self._request
    
    def _set_status(self, status):
        self._status = status

class Agent:
    RESTART_INTERVAL_CRITERIA = 30
    HEARTBEAT_INTERVAL = 2
    _automatic_built_agents = {}
    
    def __init__(self, broker_url):
        self._to_show_i_am_agent_instance = True
        self.broker_url = broker_url
        self.access_token = None
        self.agent_funcs = {}
        self.running = False
        self.interface = AgentInterface()

    def run(self, _automatic=False):
        if self.running:
            return
        self.interface.prepare(self.agent_funcs)
        self.auth = self.interface.secret_token
        self.polling_interval = 0
        self.last_heartbeat = time.time()
        if self.register_config():
            self.running = True
            threading.Thread(target=self.connect, daemon=True).start()
            threading.Thread(target=self.heartbeat).start()
            if not _automatic:
                logger.info(f"Agent {self.interface.name} has started. Press return to quit.")
                input("")
                self.goodbye()

    @classmethod
    def start(cls):
        agent_list = []
        for agent in cls._automatic_built_agents.values():
            agent.run(_automatic=True)
            agent_list.append(agent)
        logger.info(f"Press return to quit.")
        input("")
        for agent in agent_list:
            agent.goodbye()

    def goodbye(self):
        self.running = False
    
    def register_config(self):
        for _ in range(5):
            response = self.post("config", self.interface.make_config(for_registration=True), basic_auth=True)
            if "status" in response and response["status"] == "ok":
                logger.info(f"Agent {self.interface.name} has successfully connected to the broker system!")
                self.access_token = response["token"]
                logger.debug(f"TOKEN {self.access_token}")
                return True
            elif "status" in response and response["status"] == "error":
                    logger.error(response["error_msg"])
                    break
            else:
                logger.warning("Cannot connect to the broker system.")
            time.sleep(3)
        logger.error("Stop try connecting to the broker system.")
        return False

    def heartbeat(self):
        restart_timer = None
        while self.running:
            if time.time() - self.last_heartbeat > self.RESTART_INTERVAL_CRITERIA:
                if restart_timer is None:
                    restart_timer = time.time()
                elif time.time() - restart_timer >= self.RESTART_INTERVAL_CRITERIA:
                    restart_timer = None
                    logger.info(f"Automatic reconnection...")
                    threading.Thread(target=self.connect, daemon=True).start()
            else:
                restart_timer = None
            time.sleep(self.HEARTBEAT_INTERVAL)

    def connect(self):
        first_time_flag = True
        while self.running:
            self.last_heartbeat = time.time()
            try:
                messages = self.check_msgbox()
                if first_time_flag:
                    first_time_flag = False
                    
                if len(messages) > 0:
                    pass
                for message in messages:
                    threading.Thread(target=self.process_message, args=[message], daemon=True).start()
            except Exception:
                logger.exception(traceback.format_exc())
            time.sleep(self.polling_interval)

    def check_msgbox(self):
        response = self.get(f"msgbox")
        if len(response) > 0:
            return response["messages"]
        return []

    def process_message(self, message):
        try:
            logger.debug(f"Message: {message}")
            if "msg_type" not in message or "body" not in message:
                logger.exception(f"Wrong message format: {message}")
                return
            if message["msg_type"] == "negotiation_request":
                self.process_negotiation_request(message["body"])
            if message["msg_type"] == "negotiation":
                self.process_negotiation(message["body"])
            if message["msg_type"] == "contract":
                self.process_contract(message["body"])
        except:
            logger.exception(traceback.format_exc())

    def process_negotiation_request(self, msg):
        negotiation_id = msg["negotiation_id"]
        response = self.interface.make_config()
        msg = "need_revision"
        self.post("negotiation/response", {"msg": msg, "negotiation_id": negotiation_id, "response": response})

    def process_negotiation(self, msg):
        negotiation_id = msg["negotiation_id"]
        response = self.interface.make_config()
        request = msg["request"]
        msg, input_response = self.interface.validate(request)
        response["input"] = input_response
        if msg == "ok" and self.interface.has_func("negotiation"):
            msg, response = self.interface.func_dict["negotiation"](request, response)
            if msg not in ["ok", "need_revision", "ng"]:
                logger.exception(f"Negotation func in {self.interface.name} returns a wrong msg: should be one of 'ok', 'need_revision' or 'ng'")

        if msg == "ok" and self.interface.has_func("charge_func"):
            response["charge"] = int(self.interface.func_dict["charge_func"](input_response))

        self.post("negotiation/response", {"msg": msg, "negotiation_id": negotiation_id, "response": response})

    def process_contract(self, msg):
        st = time.time()
        negotiation_id = msg["negotiation_id"]
        request = msg["request"]
        job = Job(self, negotiation_id, request)
        try:
            self.post("contract/accept", {"negotiation_id": negotiation_id})
            job._set_status("running")
            job.msg(f"{self.interface.name} starts running...")
        
            result = self.interface.func_dict["job_func"](job)
            logger.debug(f"JOB RETURN VALUE: {result}")
            if result is None:
                result = {}
            job._set_status("done")
            job.report(msg="Job done.", progress=1, result=result)
        except:
            logger.exception(traceback.format_exc())
            job._set_status("error")
            job.report(msg="Error occured during the job.", progress=-1)
        logger.debug(f"{negotiation_id} takes {time.time()-st:.3f} s.")
    
    def header(self, basic_auth=False, upload=False):
        if upload:
            headers = {}
        else:
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if basic_auth:
            headers.update({"authorization": f"Basic {self.auth}"})
        elif self.access_token:
            headers.update({"authorization": f"Token {self.access_token}"})

        return headers

    def post(self, uri, payload, basic_auth=False):
        try:
            response = requests.post(f"{self.broker_url}/api/v1/agent/{uri}", json=payload, headers=self.header(basic_auth))
        except requests.exceptions.ConnectionError:
            return {}

        if response.status_code == 401 and not basic_auth:
            assert self.register_config()
            return self.post(uri, payload)
        elif response.status_code != 200:
            logger.exception(f"{response.status_code}: {uri} {payload}")
            return {}
        return response.json()

    def get(self, uri, basic_auth=False):
        try:
            response = requests.get(f"{self.broker_url}/api/v1/agent/{uri}", headers=self.header(basic_auth))
        except requests.exceptions.ConnectionError:
            if self.polling_interval < 10:
                self.polling_interval += 1
            return {}

        if response.status_code == 401 and not basic_auth:
            assert self.register_config()
            return self.get(uri)
        elif response.status_code != 200:
            logger.exception(response.status_code)
            if self.polling_interval < 10:
                self.polling_interval += 1
            return {}
        self.polling_interval = 0
        return response.json()
    
    def upload(self, file_type, binary_data):
        file_name = "__file_name__"
        mime_dict = {"png": "image/png", "gif": "image/gif", "jpeg": "image/jpeg", "csv": "text/csv", "pdf": "application/pdf",
                    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"}
        assert file_type in mime_dict
        files = {file_type: (file_name, binary_data, mime_dict[file_type])}
        try:
            response = requests.post(f"{self.broker_url}/api/v1/agent/upload", headers=self.header(upload=True), files=files)
        except requests.exceptions.ConnectionError:
            return {}
        return response.json()


    def register_func(self, func_name, func):
        self.agent_funcs[func_name] = func

    ##### wrapper functions #####
    def config(self, func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        self.register_func("make_config", wrapper)
        return wrapper

    def negotiation(self, func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        self.register_func("negotiation", wrapper)
        return wrapper

    def charge_func(self, func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        self.register_func("charge_func", wrapper)
        return wrapper

    def job_func(self, func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        self.register_func("job_func", wrapper)
        return wrapper
    
    @classmethod
    def _automatic_run(cls):
        agent_list = []
        for agent in cls._automatic_built_agents.values():
            agent.run(_automatic=True)
            agent_list.append(agent)
        return agent_list
    
    @classmethod
    def _is_automatic_mode(cls):
        return len(cls._automatic_built_agents) > 0

    @classmethod
    def make(cls, name, **agent_kwargs):
        def make_func(func):
            # automatic_flag = "_automatic" in agent_kwargs and agent_kwargs["_automatic"]
            agent = AgentConstructor.make(name=name, job_func=func, kwargs=agent_kwargs)
            # agent.run(_automatic=automatic_flag)

            def wrapper(*args, **kwargs):
                logger.warning("Direct call of the agent job function for the start up will be disabled in future. Change it to Agent.start().")
                cls.start()
                return agent
            
            cls._automatic_built_agents[name] = agent
            return wrapper
        return make_func

    @classmethod
    def add_config(cls, broker_url=None, secret_token=None):
        config_dict = {}
        if broker_url is not None:
            config_dict["broker_url"] = broker_url
        if secret_token is not None:
            config_dict["secret_token"] = secret_token
        def add_config_func(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            wrapper._additional_config = config_dict
            wrapper._original_keys = list(inspect.signature(func).parameters)
            return wrapper
        return add_config_func
    
    ##### interface for agent interface #####
    @property
    def input(self):
        return self.interface.input
    @property
    def output(self):
        return self.interface.output
    @property
    def condition(self):
        return self.interface.condition
    @property
    def secret_token(self):
        return self.interface.secret_token
    @secret_token.setter
    def secret_token(self, token):
        self.interface.secret_token = token
    @property
    def name(self):
        return self.interface.name
    @name.setter
    def name(self, name):
        self.interface.name = name
    @property
    def convention(self):
        return self.interface.convention
    @convention.setter
    def convention(self, convention):
        self.interface.convention = convention
    @property
    def description(self):
        return self.interface.description
    @description.setter
    def description(self, description):
        self.interface.description = description
    @property
    def charge(self):
        return self.interface.charge
    @charge.setter
    def charge(self, charge):
        self.interface.charge = charge

class AgentConstructor:
    def __init__(self, name, job_func, kwargs):
        self.name = name
        self.job_func = job_func
        self.kwargs = kwargs.copy()
        self.config = {}
        self.config_changed = False
        self.agent = None
    
    @classmethod
    def make(cls, name, job_func, kwargs):
        constructor = cls(name, job_func, kwargs)
        constructor.load_config()
        constructor.config["name"] = name
        constructor.fill_config()
        if constructor.config_changed:
            constructor.dump_config()
        if not ("skip_config" in kwargs and kwargs["skip_config"]):
            constructor.investigate_job_func()
            constructor.dump_config()
        
        constructor.agent = Agent(constructor.config["broker_url"])
        
        constructor.agent.register_func("make_config", constructor.make_config_func)
        constructor.agent.register_func("job_func", constructor.agent_job_func)
        return constructor.agent
    
    def investigate_job_func(self):
        input_params = self.fill_input_params()
        if self.config_changed:
            self.dump_config()
        if "job" in self.job_func_keys:
            input_params["job"] = DummyJob(input_params, {"broker_url": self.config["broker_url"], "secret_token": self.config["secret_token"]})
        result = self.job_func(**input_params)
        self.fill_output_format(result)
    
    def fill_input_params(self):
        if "input" not in self.config:
            self.config["input"] = {"@keys": []}
        if "condition" not in self.config:
            self.config["condition"] = {"@keys": []}
        container = TemplateContainer("input")
        updated = False
        keys_to_remove = set(self.config["input"]["@keys"])
        default_value_dict = {}
        for key in self.job_func_keys:
            if key in ["job"]:
                continue
            if key in keys_to_remove:
                keys_to_remove.discard(key)
            if key not in self.config["input"]["@keys"]:
                if not updated:
                    print("")
                    print("--- Input ---")
                updated = True
                setattr(container, key, self.ask_input_format(key))
                if container[key].type in ["number", "string"]:
                    default_value_dict[key] = container[key].constraint_dict["default"]
                elif container[key].type in ["choice"]:
                    default_value_dict[key] = container[key].constraint_dict["choices"][0]
                self.config_changed = True
            else:
                if "default" in self.config["input"]["@constraints"][key]:
                    default_value_dict[key] = self.config["input"]["@constraints"][key]["default"]
                elif "choices" in self.config["input"]["@constraints"][key]:
                    default_value_dict[key] = self.config["input"]["@constraints"][key]["choices"][0]
        if updated:
            self.merge_config_and_container("input", container)
        self.remove_unused_keys("input", keys_to_remove)
        return default_value_dict
    
    def merge_config_and_container(self, item_type, container):
        template_dict = container._get_template() 
        for key, value in template_dict.items():
            assert key.startswith("@"), "Property keys should start with @"
            if isinstance(value, dict):
                if key not in self.config[item_type]:
                        self.config[item_type][key] = {}
                self.config[item_type][key].update(value)
            elif isinstance(value, list):
                if key not in self.config[item_type]:
                        self.config[item_type][key] = []
                s = set(self.config[item_type][key])
                self.config[item_type][key] = list(s.union(value))

    def remove_unused_keys(self, item_type, keys_to_remove):
        if len(keys_to_remove) == 0:
            return
        for property_key in self.config[item_type]:
            for key in keys_to_remove:
                print(item_type, property_key, self.config[item_type][property_key])
                if isinstance(self.config[item_type][property_key], dict):
                    if key in self.config[item_type][property_key]:
                        del self.config[item_type][property_key][key]
                if isinstance(self.config[item_type][property_key], list):
                    s = set(self.config[item_type][property_key])
                    s.discard(key)
                    self.config[item_type][property_key] = list(s)
    
    def fill_output_format(self, result):
        if "output" not in self.config:
            self.config["output"] = {"@keys": []}
        updated = False
        keys_to_remove = set(self.config["output"]["@keys"])
        container = TemplateContainer("output")
        for key, value in result.items():
            if key in keys_to_remove:
                keys_to_remove.discard(key)
            if key not in self.config["output"]["@keys"] or (isinstance(value, pd.DataFrame) and any([c not in self.config["output"]["@unit"] for c in value.columns])):
                if not updated:
                    print("")
                    print("--- Output ---")
                updated = True
                setattr(container, key, ValueTemplate.guess_from_value(value, unit_callback_func=self.ask_output_format, key=key))
        if updated:
            self.merge_config_and_container("output", container)
        self.remove_unused_keys("output", keys_to_remove)
        
    
    def ask_input_format(self, key):
        while True:
            value_type = input(f"Select the value type of \"{key}\" ('n':Number, 's': String, 'c': Choice):")
            if value_type in ["n", "s", "c"]:
                break
        unit = None
        if value_type in ["n", "c"]:
            unit = input(f"--> Unit of \"{key}\" (empty if none):")
            if len(unit) == 0:
                unit = None    
        if value_type == "n":
            default_value = float(input(f"--> Default value of \"{key}\":"))
            print(f"== {key}: {default_value} {'('+unit+')' if unit is not None else ''} ==")
            print("")
            return Number(value=default_value, unit=unit)
        elif value_type == "c":
            choices = input(f"--> Choices separated by a comma of \"{key}\":")
            choices = [c.strip() for c in choices.split(",")]
            print(f"== {key}: {choices} {'('+unit+')' if unit is not None else ''}")
            print("")
            return Choice(choices=choices, unit=unit)
        elif value_type == "s":
            default_value = input(f"--> Default value of \"{key}\":")
            print(f"== {key}: {default_value} {'('+unit+')' if unit is not None else ''} ==")
            print("")
            return String(string=default_value)
        
    
    def ask_output_format(self, key):
        unit = input(f"Unit of \"{key}\" (empty if none):")
        print("")
        return unit

    def load_config(self):
        self.config_changed = False
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        except:
            self.config = {}

    def fill_config(self):
        broker_url = self.fill_config_item("broker_url")
        assert broker_url.startswith("http"), "broker_url should be properly specified."
        secret_token = self.fill_config_item("secret_token")
        assert len(secret_token) > 0, "secret_token should be set"
        charge = self.fill_config_item("charge", int)
        assert charge > 0, "charge should be larger than 0"
        _ = self.fill_config_item("description")
        

    def fill_config_item(self, key, as_type=str):
        if hasattr(self.job_func, "_additional_config") and key in getattr(self.job_func, "_additional_config"):
            self.config[key] = getattr(self.job_func, "_additional_config")[key]
        elif key in self.kwargs:
            if key in self.config and self.config[key] == as_type(self.kwargs[key]):
                return self.config[key]
            self.config[key] = as_type(self.kwargs[key])
            self.config_changed = True
            

        if key not in self.config:
            user_input = input(f"{key}:")
            self.config[key] = as_type(user_input)
            self.config_changed = True
        return self.config[key]
    
    def make_config_func(self):
        assert self.agent is not None, "Agent has not been properly prepared."
        keys = ["name", "secret_token", "charge", "description"]
        for key in keys:
            setattr(self.agent, key, self.config[key])

        item_types = ["input", "output", "condition"]
        for item_type in item_types:
            getattr(self.agent, item_type)._load(self.config[item_type])

    def agent_job_func(self, job):
        assert self.agent is not None, "Agent has not been properly prepared."
        input_params = self.job_to_params(job)
        if "estimated_time" in self.kwargs:
            job.periodic_report(self.kwargs["estimated_time"])
        result = self.job_func(**input_params)
        return result

    def job_to_params(self, job):
        input_keys = self.job_func_keys
        params = {key:job[key] for key in input_keys if key in job}
        if "job" in input_keys:
            params["job"] = job
        return params

    def dump_config(self):
        os.makedirs("configs", exist_ok=True)

        with open(self.config_path, "w") as f:
            json.dump(self.config, f)
        self.config_changed = False

    @property
    def job_func_keys(self):
        if hasattr(self.job_func, "_original_keys"):
            return getattr(self.job_func, "_original_keys")
        return list(inspect.signature(self.job_func).parameters)

    @property
    def config_path(self):
        return os.path.join("configs", f"{self.name}.json")


class Broker:
    def __init__(self, job = None, broker_url=None, auth=None):
        if job is None:
            assert broker_url is not None and auth is not None
            self.broker_url = broker_url
            self.auth = auth
        elif isinstance(job, Job) or hasattr(job, "_to_show_i_am_job_class"):
            self.broker_url = job._agent.broker_url
            self.auth = job._agent.interface.secret_token
        else:
            raise Exception

    def ask(self, agent_id, request):
        response = self.negotiate(agent_id, request)
        if "negotiation_id" not in response:
            raise Exception(f"Cannot communicate with Agent {agent_id}")

        negotiation_id = response["negotiation_id"]
        response = self.contract(negotiation_id)
        if "status" not in response:
            raise Exception(f"Server error")
        if response["status"] == "error":
            raise Exception(f"Cannot make a contract with Agent {agent_id}: {response['error_msg']}")
        result = self.get_result(negotiation_id)

        return result

    def negotiate(self, agent_id, request):
        response = self.post("negotiate", {"agent_id": agent_id, "request": request})
        return response

    def contract(self, negotiation_id):
        response = self.post("contract", {"negotiation_id": negotiation_id})
        return response

    def get_result(self, negotiation_id):
        msg = ""
        while True:
            response = self.get(f"result/{negotiation_id}")
            assert len(response) > 0, "Bad response error"
            if response["msg"] != msg:
                msg = response["msg"]
                logger.debug(msg)
            if response["status"] in ["done", "error"]:
                break
            time.sleep(1)
        if response["status"] == "error":
            raise Exception(f"Error response from agent: {response['msg']}")
        return response

    @property
    def header(self):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        headers.update({"authorization": f"Basic {self.auth}"})
        return headers


    def post(self, uri, payload):
        try:
            logger.debug
            response = requests.post(f"{self.broker_url}/api/v1/client/{uri}", json=payload, headers=self.header)
        except requests.exceptions.ConnectionError:
            logger.exception(traceback.format_exc())
        if response.status_code != 200:
            logger.exception(response.status_code)
            return {}
        return response.json()

    def get(self, uri):
        try:
            response = requests.get(f"{self.broker_url}/api/v1/client/{uri}", headers=self.header)
        except requests.exceptions.ConnectionError:
            logger.exception(traceback.format_exc())
            return {}

        if response.status_code != 200:
            logger.exception(response.status_code)
            return {}
        return response.json()

class AgentManager:
    WATCHING_INTERVAL = 5
    def __init__(self, dir_path=""):
        self.dir_path = dir_path
        self.agents = {}
        self.start_watching_loop()
    
    def start_watching_loop(self):
        while True:
            try:
                self.dog_watching()
                time.sleep(self.WATCHING_INTERVAL)
            except KeyboardInterrupt:
                logger.info("Automatic agent runner closing...")
                break
        for k in self.agents.keys():
            self.stop(k)

    def dog_watching(self):
        
        exisiting_files = set(glob.glob(os.path.join(self.dir_path, "*.py")))
        current_files = set(self.agents.keys())
        new_files = exisiting_files - current_files
        removed_files = current_files - exisiting_files
        ongoing_files = current_files & exisiting_files
        for file in new_files:
            self.load(file)
        for file in ongoing_files:
            self.check_for_update(file)
        for file in removed_files:
            self.stop(file)
            self.agents.pop(file)
    
    def run_module(self, module):
        def is_agent(obj):
            return hasattr(obj, "_to_show_i_am_agent_instance")
        def is_automatic_agent(obj):
            return hasattr(obj, "_is_automatic_mode") and getattr(obj, "_is_automatic_mode")()
        for key in module.__dir__():
            if is_agent(getattr(module, key)):
                agent = getattr(module, key)
                agent.run(_automatic=True)
                return agent
            elif is_automatic_agent(getattr(module, key)):
                agent_class = getattr(module, key)
                return getattr(agent_class, "_automatic_run")()
        return None

    def load(self, file):
        self.agents[file] = {"mtime": os.path.getmtime(file)}
        try:
            module_name = file.replace(".py", "").replace(os.path.sep, ".")
            module = importlib.import_module(module_name)
            self.agents[file]["module"] = module
            agent = self.run_module(module)
            if agent is not None:
                self.agents[file]["agent"] = agent
                if isinstance(agent, list):
                    logger.info(f"Agent {[x.interface.name for x in agent]} has started!")
                else:
                    logger.info(f"Agent {agent.interface.name} has started!")
        except:
            logger.exception(traceback.format_exc())

    def check_for_update(self, file):
        try:
            if os.path.getmtime(file) != self.agents[file]["mtime"]:
                self.agents[file]["mtime"] = os.path.getmtime(file)
                if "module" not in self.agents[file]:
                    self.load(file)
                    return
                if "agent" in self.agents[file]:
                    self.stop(file)
                    time.sleep(Agent.HEARTBEAT_INTERVAL)
                    
                module = importlib.reload(self.agents[file]["module"])
                self.agents[file]["module"] = module
                agent = self.run_module(module)
                if agent is not None:
                    self.agents[file]["agent"] = agent
                    logger.info(f"Agent {agent.interface.name} has started!")
        except:
            logger.exception(traceback.format_exc())
    
    def stop(self, file):
        try:
            if "agent" in self.agents[file]:
                if isinstance(self.agents[file]["agent"], list):
                    for agent in self.agents[file]["agent"]:
                        agent.goodbye()
                else:
                    self.agents[file]["agent"].goodbye()
        except:
            logger.exception(traceback.format_exc())


def batch_run():
    AgentManager()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "batch_run":
        batch_run()