import sys
from distutils.version import LooseVersion
from jennifer.agent import jennifer_agent

__hooking_module__ = 'urllib3'
__minimum_python_version__ = LooseVersion("2.7")
_original_urllib3_poolmanager_request = None
_original_urllib3_poolmanager_urlopen = None

global parse_url_func3


def parse_url2(url):
    from urlparse import urlparse
    return urlparse(url)


def parse_url3(url):
    from urllib import parse
    return parse.urlparse(url)


def wrap_request(urlrequest):
    global parse_url_func3

    if sys.version_info.major == 3:
        parse_url_func3 = parse_url3
    else:
        parse_url_func3 = parse_url2

    def handler(*args, **kwargs):
        transaction = None
        url = None

        try:
            from urllib3 import response

            agent = jennifer_agent()
            transaction = agent.current_transaction()
            url = kwargs.get('url') or args[2]

            if transaction is not None:
                o = parse_url_func3(url)
                transaction.profiler.external_call(
                    protocol=o.scheme,
                    host=o.hostname,
                    port=o.port or 80,
                    url=url,
                    caller='urllib3.PoolManager')
        except:
            pass

        ret = urlrequest(*args, **kwargs)

        try:
            if isinstance(ret, response.HTTPResponse):
                transaction.profiler.end(
                    message='urllib3.request(url=%s,response=%s)' % (url, ret.status)
                )
            else:
                transaction.profiler.end()
        except:
            pass

        return ret
    return handler


def unhook(urllib3_module):
    global _original_urllib3_poolmanager_request
    global _original_urllib3_poolmanager_urlopen

    if _original_urllib3_poolmanager_request is not None:
        urllib3_module.poolmanager.PoolManager.request = _original_urllib3_poolmanager_request

    if _original_urllib3_poolmanager_urlopen is not None:
        urllib3_module.poolmanager.PoolManager.urlopen = _original_urllib3_poolmanager_urlopen


def hook(urllib3_module):
    if not sys.version_info.major == 3:
        return

    global _original_urllib3_poolmanager_request
    global _original_urllib3_poolmanager_urlopen

    _original_urllib3_poolmanager_request = urllib3_module.poolmanager.PoolManager.request
    _original_urllib3_poolmanager_urlopen = urllib3_module.poolmanager.PoolManager.urlopen

    urllib3_module.poolmanager.PoolManager.request = wrap_request(urllib3_module.poolmanager.PoolManager.request)
    urllib3_module.poolmanager.PoolManager.urlopen = wrap_request(urllib3_module.poolmanager.PoolManager.urlopen)
