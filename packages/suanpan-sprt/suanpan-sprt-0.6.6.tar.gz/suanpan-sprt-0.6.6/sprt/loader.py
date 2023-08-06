import json
import logging
import inspect
import pathlib
import importlib
import importlib.util
from quart import current_app
from .arguments import init_arg_from_arg_spec, init_return_from_value, DEFAULT_DATA_SUBTYPE_ARGS_MAP
from .storage import Storage
from .exceptions import ParamsArgError, InvocationFunctionError
from .log import NodeStreamHandler, LogkitHandler


class NodeFunction(object):
    def __init__(self, user_id, app_id, node_id, working_dir, filename, function='main'):
        file = pathlib.Path(filename)
        self.name = file.stem
        self.location = pathlib.Path(working_dir) / filename
        self.function = function
        self.module = self.load_module()
        self.context = RuntimeContext(user_id, app_id, node_id)
        self.input_arguments = []
        self.has_context = False
        self.load_validator()
        self._logkit = self._init_logkit(app_id, node_id)
        self.context.log = self._logkit
        self._logkit_handler = None

    def load_module(self):
        if not self.location.is_file():
            raise Exception(f'invalid component file: {self.location}')

        spec = importlib.util.spec_from_file_location(self.name, self.location)
        if spec is None:
            raise Exception(f'invalid component spec: {self.location}')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def load_validator(self):
        has_context = False

        func = getattr(self.module, self.function)
        arg_spec = inspect.getfullargspec(func)
        for index, a in enumerate(arg_spec.args):
            if a == 'context':
                if index != len(arg_spec.args) - 1:
                    raise ParamsArgError('context MUST be the last argument of function')

                has_context = True
                continue

            arg_class = init_arg_from_arg_spec(a, arg_spec)
            arg = arg_class(a, arg_spec=arg_spec)
            self.input_arguments.append(arg)

        if has_context or arg_spec.varkw is not None:
            self.has_context = True
        else:
            raise ParamsArgError('function MUST have a "context" argument')

    async def call_func(self, request_id, args, params):
        in_slot = []

        func = getattr(self.module, self.function)
        arg_spec = inspect.getfullargspec(func)
        for index, a in enumerate(arg_spec.args):
            if a == 'context':
                continue

            arg = self.input_arguments[index]

            inx = f'in{index + 1}'
            value = args.get(inx)
            value = arg.load(value)

            in_slot.append(value)

        self.context.reset(request_id, params)
        try:
            if inspect.iscoroutinefunction(func):
                ret = await func(*in_slot, context=self.context)
            else:
                ret = func(*in_slot, context=self.context)

            if isinstance(ret, tuple):
                return {f'out{index + 1}': init_return_from_value(r, arg_spec, index)(
                    f'out{index + 1}', request_id=request_id).save(r)
                        for index, r in enumerate(ret)}
            else:
                return {'out1': init_return_from_value(ret, arg_spec, 0)(f'out{1}', request_id=request_id).save(ret)}
        except Exception as e:
            raise InvocationFunctionError(f'call function: {e}')

    def update_logkit(self, logkit=None):
        if logkit is None:
            self._logkit.removeHandler(self._logkit_handler)
        else:
            if self._logkit_handler and logkit.uri != self._logkit_handler.uri:
                self._logkit.removeHandler(self._logkit_handler)
                self._logkit_handler = None

            if self._logkit_handler is None:
                logging.info('setup logkit handler: %s', logkit.uri)
                lh = LogkitHandler(logkit.uri, logkit.namespace, logkit.path, logkit.events_append)
                lh.setLevel(logkit.logs_level.upper())
                self._logkit.addHandler(lh)
                self._logkit_handler = lh
                # self._logkit.setLevel(logkit.logs_level.upper())

    @staticmethod
    def _init_logkit(app_id, node_id):
        name = f'logkit_{app_id}_{node_id}'
        logger = logging.getLogger(name)
        logger.propagate = False

        if len(logger.handlers) > 0:
            return logger

        formatter = logging.Formatter('%(asctime)s :: [%(levelname)-8s] %(message)s')
        sh = NodeStreamHandler()
        sh.setLevel('DEBUG')
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        return logger

    def __del__(self):
        # os.remove(self.location)
        if self._logkit_handler:
            current_app.logger.info('close logkit handler: %s', self._logkit_handler.uri)
            self._logkit_handler.close()
        self._logkit.handlers.clear()
        del self.module


class RuntimeContext(object):
    def __init__(self, user_id, app_id, node_id):
        self.request_id = None
        self.user_id = user_id
        self.app_id = app_id
        self.node_id = node_id
        self.params = NodeParams()
        self.log = None
        self.storage = Storage.get_instance()

    def reset(self, request_id, params):
        self.request_id = request_id
        if not isinstance(params, dict):
            params = json.loads(params)
        self.params._data = params

    def __repr__(self):
        return f'<Context: request_id {self.request_id}>'


class NodeParams(object):
    def __init__(self):
        self._data = {}

    def meta(self, name):
        return self._data.get(name)

    def __getattr__(self, name):
        param = self.meta(name)
        if not param:
            return param

        _type = param.get('type')
        _value = param.get('value')

        arg_class = DEFAULT_DATA_SUBTYPE_ARGS_MAP.get(_type)
        return arg_class(name).load(_value)

    def __getitem__(self, item):
        return self.__getattr__(item)
