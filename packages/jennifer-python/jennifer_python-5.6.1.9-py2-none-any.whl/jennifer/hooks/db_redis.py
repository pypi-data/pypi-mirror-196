import os

from jennifer.agent import jennifer_agent
import json
from distutils.version import LooseVersion

__hooking_module__ = 'redis'
__minimum_python_version__ = LooseVersion("2.7")
_original_redis_execute_command = None


def format_command(*args):
    cmd = args[0]
    parameters = [cmd]
    for arg in args[1:]:
        p = json.dumps(arg)
        parameters.append(p)

    return ' [REDIS] ' + ' '.join(parameters)


def wrap_execute_command(origin):

    def handler(self, *args, **kwargs):
        try:
            agent = jennifer_agent()
            transaction = agent.current_transaction()
            if transaction is not None:
                message = format_command(*args)
                transaction.profiler.message(message)
        except Exception as e:
            print(os.getpid(), 'jennifer.exception', 'db.redis', e)

        ret = origin(self, *args, **kwargs)
        return ret

    return handler


def unhook(redis_module):
    global _original_redis_execute_command
    if _original_redis_execute_command is not None:
        redis_module.Redis.execute_command = _original_redis_execute_command


def hook(redis_module):
    global _original_redis_execute_command
    _original_redis_execute_command = redis_module.Redis.execute_command
    redis_module.Redis.execute_command = wrap_execute_command(redis_module.Redis.execute_command)
