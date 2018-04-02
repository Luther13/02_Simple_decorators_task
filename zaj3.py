from functools import wraps
import json
import logging, inspect


# Zadanie 1
def add_tag(input):
    def really_add(input_fun):
        @wraps(input_fun)
        def adder(*args,**kwargs):
            result = input_fun(*args, **kwargs)
            return '<{}>{}</{}>'.format(input, result, input)
        return adder
    return really_add


@add_tag('h1')
def write(*args,**kwargs):
    return f"Elko melko"


# Zadanie 2
def validate_json(*args):
    def inner_validate(input_fun):
        def checker(*args1):
            nonlocal args
            if len(json.loads(args1[0])) != len(args):
                raise ValueError()
            for e in args:
                if json.loads(args1[0]).get(e) is None:
                    raise ValueError()
        return checker
    return inner_validate


@validate_json('first_name', 'last_name', 'age')
def jsoner(json):
    return len(json)


# Zadanie 3 DOPYTAC, BO NIE CZAJE
def log_this(logger, level, format):
    def real_decorator(to_be_decorated):
        def wrapper(*args, **kwargs):
            result = to_be_decorated(*args, **kwargs)
            args_as_string = ()
            for i in range(len(args)):
                temp = str(args[i])
                temp_tuple = (temp,)
                args_as_string = args_as_string + temp_tuple
            arguments = args_as_string
            for key, value in kwargs.items():
                temp = f'{key}={value}'
                temp_tuple = (temp,)
                arguments = arguments + temp_tuple
            print(logger.info(format, to_be_decorated.__name__, arguments, result))
            return result
        return wrapper
    return real_decorator


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@log_this(logger, level=logging.INFO, format='%s: %s -> %s')
def my_func(a, b, c=None, d=False):
    return 'Wow!'


my_func(1,2,d=True)