import traceback
from logger_local_python_package.MessageSeverity import MessageSeverity
from logger_local_python_package.Writer import Writer
import os
import json
import inspect
import requests
import logzio
from logzio.handler import LogzioHandler

debug = os.getenv("debug")
logzio_token = os.getenv("LOGZIO_TOKEN")
logzio_url = "https://listener.logz.io:8071"


class LoggerService:

    def __init__(self):
        self._writer = Writer()
        self.fields = self.get_logger_table_fields()
        for field in self.fields:
            setattr(self, field, None)
        self.logzio_handler = LogzioHandler(token=logzio_token, url=logzio_url)

    def init(self, *args, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {args} kwargs= {kwargs})')
        if args and 'object' in kwargs:
            self.insertVariables(**kwargs)
            kwargs['object']['severity_id'] = MessageSeverity.Init.value
            kwargs['object']['severity_name'] = MessageSeverity.Init.name
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self._writer.addMessageAndPayload(args[0], **kwargs)
            self.send_to_logzio(kwargs['object'])
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Init.value)
                logzio_data = {
                    'severity_id': MessageSeverity.End.value,
                    'message': args[0]
                }
                logzio_data = self.insert_to_payload_extra_vars(
                    object=logzio_data)
                self.insert_To_object(**logzio_data)
                self.send_to_logzio(logzio_data.get("object"))
            else:
                if 'object' in kwargs:
                    self.insertVariables(**kwargs)
                    kwargs['object']['severity_id'] = MessageSeverity.Init.value
                    kwargs['object']['severity_name'] = MessageSeverity.Init.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self._writer.add(**kwargs)
                    self.send_to_logzio(kwargs['object'])

    def start(self, *args, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {args} kwargs= {kwargs})')
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Start.value
            kwargs['object']['severity_name'] = MessageSeverity.Start.name
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            self._writer.addMessageAndPayload(args[0], **kwargs)
            self.send_to_logzio(kwargs['object'])
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Start.value)
                logzio_data = {
                    'message': args[0],
                    'severity_id': MessageSeverity.Init.value
                }
                logzio_data = self.insert_to_payload_extra_vars(
                    object=logzio_data)
                self.insert_To_object(**logzio_data)
                self.send_to_logzio(logzio_data.get("object"))
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Start.value
                    kwargs['object']['severity_name'] = MessageSeverity.Start.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    self._writer.add(**kwargs)
                    self.send_to_logzio(kwargs['object'])

    def end(self, *args, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {args} kwargs= {kwargs})')
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.End.value
            kwargs['object']['severity_name'] = MessageSeverity.End.name
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            self._writer.addMessageAndPayload(args[0], **kwargs)
            self.send_to_logzio(kwargs['object'])
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.End.value)
                logzio_data = {
                    'severity_id': MessageSeverity.End.value,
                    'message': args[0]
                }
                logzio_data = self.insert_to_payload_extra_vars(
                    object=logzio_data)
                self.insert_To_object(**logzio_data)
                self.send_to_logzio(logzio_data.get("object"))
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.End.value
                    kwargs['object']['severity_name'] = MessageSeverity.End.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    self._writer.add(**kwargs)
                    self.send_to_logzio(kwargs['object'])

    def exception(self, *args, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {args} kwargs= {kwargs})')
        if args and 'object' in kwargs:
            stack_trace = traceback.format_exception(
                type(kwargs['object']), kwargs['object'], kwargs['object'].__traceback__)
            object_exp = {
                'severity_id': MessageSeverity.Exception.value,
                'severty_name': MessageSeverity.Exception.name,
                'error_stack': f'{str(stack_trace)}'
            }
            object_exp = self.insert_to_payload_extra_vars(object=object_exp)
            self.insert_To_object(**object_exp)
            self._writer.addMessageAndPayload(args[0], **object_exp)
            self.send_to_logzio(object_exp['object'])
        else:
            if args:
                self._writer.add_message(
                    args[0], MessageSeverity.Exception.value)
                logzio_data = {
                    'severity_id': MessageSeverity.Error.value,
                    'severty_name': MessageSeverity.Exception.name,
                    'message': args[0]
                }
                logzio_data = self.insert_to_payload_extra_vars(
                    object=logzio_data)
                self.insert_To_object(**logzio_data)
                self.send_to_logzio(logzio_data.get("object"))
            else:
                if 'object' in kwargs:
                    stack_trace = traceback.format_exception(
                        type(kwargs['object']), kwargs['object'], kwargs['object'].__traceback__)
                    object_exp = {
                        'severity_id': MessageSeverity.Exception.value,
                        'severty_name': MessageSeverity.Exception.name,
                        'error_stack': f'{str(stack_trace)}'
                    }
                    object_exp = self.insert_to_payload_extra_vars(
                        object=object_exp)
                    self.insert_To_object(**object_exp)
                    self._writer.add(**object_exp)
                    self.send_to_logzio(object_exp['object'])

    def info(self, *args, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {args} kwargs= {kwargs})')
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Information.value
            kwargs['object']['severity_name'] = MessageSeverity.Information.name
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            self._writer.addMessageAndPayload(args[0], **kwargs)
        else:
            if args:
                self._writer.add_message(
                    args[0], MessageSeverity.Information.value)
                logzio_data = {
                    'severity_id': MessageSeverity.Information.value,
                    'message': args[0]
                }
                logzio_data = self.insert_to_payload_extra_vars(
                    object=logzio_data)
                self.insert_To_object(**logzio_data)
                self.send_to_logzio(logzio_data.get("object"))
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Information.value
                    kwargs['object']['severity_name'] = MessageSeverity.Information.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    self._writer.add(**kwargs)

    def error(self, *args, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {args} kwargs= {kwargs})')
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Error.value
            kwargs['object']['severity_name'] = MessageSeverity.Error.name
            self.insert_To_object(**kwargs)
            self._writer.addMessageAndPayload(args[0], **kwargs)
            self.send_to_logzio(kwargs['object'])
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Error.value)
                logzio_data = {
                    'severity_id': MessageSeverity.Error.value,
                    'message': args[0]
                }
                logzio_data = self.insert_to_payload_extra_vars(
                    object=logzio_data)
                self.insert_To_object(**logzio_data)
                self.send_to_logzio(logzio_data.get("object"))
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Error.value
                    kwargs['object']['severity_name'] = MessageSeverity.Error.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    self._writer.add(**kwargs)
                    self.send_to_logzio(kwargs['object'])

    def warn(self, *args, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {args} kwargs= {kwargs})')
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Error.value
            kwargs['object']['severity_name'] = MessageSeverity.Warning.name
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            self._writer.addMessageAndPayload(args[0], **kwargs)
            self.send_to_logzio(kwargs['object'])
        else:
            if args:
                self._writer.add_message(
                    args[0], MessageSeverity.Warning.value)
                logzio_data = {
                    'severity_id': MessageSeverity.Warning.value,
                    'message': args[0]
                }
                logzio_data = self.insert_to_payload_extra_vars(
                    object=logzio_data)
                self.insert_To_object(**logzio_data)
                self.send_to_logzio(logzio_data.get("object"))
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Warning.value
                    kwargs['object']['severity_name'] = MessageSeverity.Warning.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    self._writer.add(**kwargs)
                    self.send_to_logzio(kwargs['object'])

    def debug(self, *args, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {args} kwargs= {kwargs})')
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Debug.value
            kwargs['object']['severity_name'] = MessageSeverity.Debug.name
            self.insert_To_object(**kwargs)
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self._writer.addMessageAndPayload(args[0], **kwargs)
            self.send_to_logzio(kwargs['object'])
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Debug.value)
                logzio_data = {
                    'severity_id': MessageSeverity.Debug.value,
                    'message': args[0]
                }
                logzio_data = self.insert_to_payload_extra_vars(
                    object=logzio_data)
                self.insert_To_object(**logzio_data)
                self.send_to_logzio(logzio_data.get("object"))
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Debug.value
                    kwargs['object']['severity_name'] = MessageSeverity.Debug.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    self._writer.add(**kwargs)
                    self.send_to_logzio(kwargs['object'])

    def verbose(self, *args, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {args} kwargs= {kwargs})')
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
            kwargs['object']['severity_name'] = MessageSeverity.Verbose.name
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            self._writer.addMessageAndPayload(args[0], **kwargs)
            self.send_to_logzio(kwargs['object'])
        else:
            if args:
                self._writer.add_message(
                    args[0], MessageSeverity.Verbose.value)
                logzio_data = {
                    'severity_id': MessageSeverity.Verbose.value,
                    'message': args[0]
                }
                logzio_data = self.insert_to_payload_extra_vars(
                    object=logzio_data)
                self.insert_To_object(**logzio_data)
                self.send_to_logzio(logzio_data.get("object"))
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
                    kwargs['object']['severity_name'] = MessageSeverity.Verbose.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    self._writer.add(**kwargs)
                    self.send_to_logzio(kwargs['object'])

    def insertVariables(self, **object):
        object_data = object.get("object", {})
        for field in self.fields:
            setattr(self, field, object_data.get(field, getattr(self, field)))

    def insert_To_object(self, **kwargs):
        object_data = kwargs.get("object", {})
        for field in self.fields:
            if field not in object_data:
                field_value = getattr(self, field)
                if field_value is not None:
                    object_data[field] = field_value

    def get_logger_table_fields(self):
        fields = ['client_ip_v4', 'client_ip_v6', 'server_ip_v4', 'server_ip_v6', 'location_id', 'user_id',
                  'profile_id', 'activity', 'activity_id', 'message', 'record', 'payload',
                  'component_id', 'error_stack', 'severity_id', 'status_id', 'group_id', 'relationship_type_id',
                  'state_id', 'variable_id', 'variable_value_old', 'variable_value_new', 'created_user_id',
                  'updated_user_id']
        return fields

    def clean_variables(self):
        for field in self.fields:
            setattr(self, field, None)

    def insert_to_payload_extra_vars(self, **kwargs):
        fields_list = self.get_logger_table_fields()
        kwargs['object']['function'] = self.get_current_function_name()
        kwargs['object']['environment'] = os.getenv("ENVIRONMENT")
        kwargs['object']['package'] = self.get_calling_package()
        kwargs['object']['row'] = self.get_calling_line_number()
        for field in self.fields:
            if field not in kwargs['object']:
                field_value = getattr(self, field)
                if field_value is not None:
                    kwargs['object'][field] = field_value
        object_data = kwargs.get("object", {})
        object_data_payload = {key: value for key,
                               value in object_data.items()}
        object_data_record_json = json.dumps(object_data_payload)
        object_data["record"] = object_data_record_json
        object_data = {key: value for key,
                       value in object_data.items() if key in fields_list}
        kwargs["object"] = object_data

        return kwargs

    def get_current_function_name(self):
        stack = inspect.stack()
        caller_frame = stack[3]
        function_name = caller_frame.function
        return function_name

    def get_calling_package(self):
        stack = inspect.stack()
        calling_module = inspect.getmodule(stack[3].frame)
        return calling_module.__name__

    def get_calling_line_number(self):
        stack = inspect.stack()
        calling_frame = stack[3]
        line_number = calling_frame.lineno
        return line_number

    def send_to_logzio(self, data):
        if ("component_id" not in data):
            print("please enter component id")
        try:
            log_record = CustomLogRecord(
                name="log",
                level=data.get('severity_id'),
                pathname=logzio_url,
                lineno=data.get("row"),
                msg=data.get('record'),
                args=data,
            )
            self.logzio_handler.emit(log_record)
        except Exception as e:
            print(f"Failed to send log to Logz.io: {e}")


class CustomLogRecord:
    def __init__(self, name, level, pathname, lineno, msg, args):
        self.name = name
        self.levelname = level
        self.pathname = pathname
        self.lineno = lineno
        self.msg = msg
        self.args = args
        self.exc_info = None
        self.exc_text = None
        self.stack_info = None

    def getMessage(self):
        msg = str(self.msg)
        if self.args:
            try:
                msg = self.msg.format(*self.args)
            except Exception as e:
                pass
        return msg
