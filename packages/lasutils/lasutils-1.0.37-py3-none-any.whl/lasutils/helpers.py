import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Union, Dict, List, Callable
from dateutil.parser import parse, ParserError
import time
from lasutils.exceptions import MissingEnvironmentVariable, ErroneousEnvironmentVariable


def get_env(
    env_var: str,
    default=None,
    required: bool = False,
    valid_options: list = None,
    is_path: bool = False,
    is_json: bool = False,
    is_datetime: bool = False,
    is_list: bool = False,
):
    env = os.getenv(env_var, default)
    if required and not env:
        logging.error(f"Environment variable {env_var} is required.")
        raise MissingEnvironmentVariable(f"Environment variable {env_var} is required.")
    if not env:
        return default
    if valid_options and env not in valid_options:
        raise ErroneousEnvironmentVariable(
            f"{env} not a valid option: {valid_options}."
        )
    if is_path:
        return str(Path(env).absolute())
    if is_json:
        if env:
            return json.loads(env)
        return {}
    if is_datetime:
        try:
            return parse(env)
        except ParserError as err:
            raise ErroneousEnvironmentVariable(
                f"Cannot parse date: {env}, Error: {err}"
            )
    if is_list:
        return env.split(".") if type(env) == str else default
    return env


def get_nested(data: dict, keys: list):
    if data:
        return get_nested(data[keys[0]], keys[1:]) if keys else data
    return None


def set_nested(
    data: dict, keys: list, value: Union[str, int, float, Dict, List, Callable]
):
    if len(keys) > 1:
        if isinstance(data, list):
            for idx, _ in enumerate(data):
                set_nested(data[idx], keys, value)
        else:
            if data.get(keys[0]):
                set_nested(data[keys[0]], keys[1:], value)
    else:
        if isinstance(data, list):
            for idx, _ in enumerate(data):
                if data[idx].get(keys[0]):
                    data[idx][keys[0]] = value
        else:
            if data.get(keys[0]):
                data[keys[0]] = (
                    value(data[keys[0]]) if isinstance(value, Callable) else value
                )


def generate_hash(item: Union[Dict, str]) -> str:
    if isinstance(item, str):
        return hashlib.md5(item.encode("utf-8")).hexdigest()
    return hashlib.md5(json.dumps(item).encode("utf-8")).hexdigest()


# do_every(1,<function>,<args>)
def do_every(period, f, *args):
    def g_tick():
        t = time.time()
        while True:
            t += period
            yield max(t - time.time(), 0)

    g = g_tick()
    while True:
        try:
            time.sleep(next(g))
            f(*args)
        except KeyboardInterrupt:
            logging.info(f"Time loop interrupted.")
            break
