import inspect
import pathlib
import importlib
import importlib.util
from .arguments import init_arg_from_arg_spec, init_return_from_value, init_params_from_arg_spec
from .exceptions import ParamsArgError


class NodeFunction(object):
    def __init__(self, working_dir, filename, function='main'):
        file = pathlib.Path(filename)
        self.name = file.stem
        self.location = pathlib.Path(working_dir) / filename
        self.function = function
        self.module = self.load_module()

    def load_module(self):
        if not self.location.is_file():
            raise Exception(f'invalid component file: {self.location}')

        spec = importlib.util.spec_from_file_location(self.name, self.location)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    async def call_func(self, args, params):
        in_slot = []
        has_params = False

        func = getattr(self.module, self.function)
        arg_spec = inspect.getfullargspec(func)
        for index, a in enumerate(arg_spec.args):
            if a == 'params':
                if index != len(arg_spec.args) - 1:
                    raise ParamsArgError('params MUST be the last argument of function')

                has_params = True
                continue

            arg_class = init_arg_from_arg_spec(a, arg_spec)
            arg = arg_class(a, arg_spec=arg_spec)

            inx = f'in{index + 1}'
            value = args.get(inx)
            value = arg.load(value)

            in_slot.append(value)

        if has_params or arg_spec.varkw is not None:
            arg_class = init_params_from_arg_spec('params', arg_spec)
            arg = arg_class('params', arg_spec=arg_spec)

            params = arg.load(params)
            if inspect.iscoroutinefunction(func):
                ret = await func(*in_slot, params=params)
            else:
                ret = func(*in_slot, params=params)
        else:
            if inspect.iscoroutinefunction(func):
                ret = await func(*in_slot)
            else:
                ret = func(*in_slot)

        if isinstance(ret, tuple):
            return {f'out{index + 1}': init_return_from_value(r)(f'out{index + 1}').save(r)
                    for index, r in enumerate(ret)}
        else:
            return {'out1': init_return_from_value(ret)(f'out{1}').save(ret)}
