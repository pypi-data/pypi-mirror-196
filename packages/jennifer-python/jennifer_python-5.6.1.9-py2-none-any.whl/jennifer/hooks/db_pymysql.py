from distutils.version import LooseVersion

__hooking_module__ = 'pymysql'
__minimum_python_version__ = LooseVersion("2.7")
_original_db_connect = None


def safe_get(properties, idx, default=None):
    try:
        return properties[idx]
    except IndexError:
        return default


def connection_info(*args, **kwargs):
    host = safe_get(args, 0) or kwargs.get('host')
    port = safe_get(args, 4) or kwargs.get('port') or 3306
    database = safe_get(args, 3) or kwargs.get('database') or kwargs.get('db')
    return host, port, database


def unhook(pymysql_module):
    global _original_db_connect
    if _original_db_connect is not None:
        pymysql_module.connect = _original_db_connect


def hook(pymysql_module):
    from jennifer.wrap import db_api
    global _original_db_connect
    _original_db_connect = db_api.register_database(pymysql_module, connection_info)
