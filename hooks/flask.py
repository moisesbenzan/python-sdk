
import traceback
from blackfire.utils import function_wrapper, import_module, get_logger

log = get_logger(__name__)

def _wrap_app(instance, *args, **kwargs):
    try:
        from blackfire.middleware import FlaskMiddleware

        instance.wsgi_app = FlaskMiddleware(instance)

        log.debug("Blackfire Flask middleware enabled.")
    except Exception as e:
        log.exception(e)

def patch():
    # TODO: if already imported print warning? I did not see anyone has done
    # similar thing?
    module = import_module('flask')
    if not module:
        return False
    
    # already patched?
    if getattr(module, '_blackfire_patch', False):
        return
    setattr(module, '_blackfire_patch', True)

    try:
        module.Flask.__init__ = function_wrapper(
            module.Flask.__init__, post_func=_wrap_app
        )
        return True
    except Exception as e:
        log.exception(e)

    return False
