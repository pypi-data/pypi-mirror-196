from distutils.version import LooseVersion

__hooking_module__ = 'sqlite3'
__minimum_python_version__ = LooseVersion("2.7")
_original_db_connect = None
_original_dbapi2_connect = None


def connection_info(database, *args, **kwargs):
    return 'localhost', 0, database


def unhook(sqlite3_module):
    global _original_db_connect
    if _original_db_connect is not None:
        sqlite3_module.connect = _original_db_connect

    global _original_dbapi2_connect
    if _original_dbapi2_connect is not None:
        sqlite3_module.dbapi2.connect = _original_dbapi2_connect


def hook(sqlite3_module):
    from jennifer.wrap import db_api
    global _original_db_connect
    _original_db_connect = db_api.register_database(sqlite3_module, connection_info)

    if sqlite3_module.dbapi2 is not None:
        global _original_dbapi2_connect
        _original_dbapi2_connect = db_api.register_database(sqlite3_module.dbapi2, connection_info)
