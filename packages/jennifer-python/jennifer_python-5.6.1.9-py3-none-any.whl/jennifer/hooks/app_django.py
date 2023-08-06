from jennifer.wrap.wsgi import wrap_wsgi_app
from jennifer.agent import jennifer_agent
from jennifer.api.format import format_function
from distutils.version import LooseVersion

__hooking_module__ = 'django'
__minimum_python_version__ = LooseVersion("2.7")
__original_wsgi_handler_call = None


def unhook(django_module):
    if __original_wsgi_handler_call is not None:
        from django.core.handlers.wsgi import WSGIHandler
        WSGIHandler.__call__ = __original_wsgi_handler_call


def hook(django_module):
    from django.core.handlers.wsgi import WSGIHandler

    def wrap_wsgi_handler_class(origin_wsgi_entry_func):
        def handler(self, environ, start_response):
            resolver = None
            request = self.request_class(environ)
            if hasattr(django_module, 'urls') and hasattr(django_module.urls, 'get_resolver'):
                get_resolver = django_module.urls.get_resolver
                if hasattr(request, 'urlconf'):
                    urlconf = request.urlconf
                    resolver = get_resolver(urlconf)
                else:
                    resolver = get_resolver()
            elif hasattr(django_module.core, 'urlresolvers'):
                url_resolvers = django_module.core.urlresolvers
                settings = django_module.conf.settings
                urlconf = settings.ROOT_URLCONF
                url_resolvers.set_urlconf(urlconf)
                resolver = url_resolvers.RegexURLResolver(r'^/', urlconf)
                if hasattr(request, 'urlconf'):
                    urlconf = request.urlconf
                    url_resolvers.set_urlconf(urlconf)
                    resolver = url_resolvers.RegexURLResolver(r'^/', urlconf)

            profiler = None

            if resolver is not None:
                try:
                    agent = jennifer_agent()
                    if agent is not None:
                        profiler = agent.current_transaction().profiler

                    try:
                        resolver_match = resolver.resolve(request.path_info)
                        name = format_function(resolver_match.func)

                        if profiler is not None:
                            profiler.set_root_name(name)
                    except:
                        pass

                except:
                    if profiler is not None:
                        profiler.set_root_name(request.path_info)
                    pass

                # origin_path_info: '/static/bbs/custom.css'
                # request.path: u'/static/bbs/custom.css'
                # request.get_full_path(): u'/static/bbs/custom.css'
                # request.build_absolute_uri(): 'http://localhost:18091/static/bbs/custom.css'

            origin_result = origin_wsgi_entry_func(self, environ, start_response)
            if profiler is not None and origin_result.status_code >= 400:
                if origin_result.status_code == 404:
                    profiler.not_found("Not Found: " + environ['PATH_INFO'])
                else:
                    profiler.service_error("Service Error: " + origin_result.reason_phrase)

            return origin_result

        return handler

    global __original_wsgi_handler_call
    __original_wsgi_handler_call = WSGIHandler.__call__
    WSGIHandler.__call__ = wrap_wsgi_handler_class(WSGIHandler.__call__)
    WSGIHandler.__call__ = wrap_wsgi_app(WSGIHandler.__call__)  # , 'django.core.handlers.wsgi.WSGIHandler.__call__')
