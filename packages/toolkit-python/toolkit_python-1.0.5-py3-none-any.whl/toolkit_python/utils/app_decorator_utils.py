from functools import wraps
from flask import current_app, request
from .app_exception_utils import ApiException


# ==============================


def tenant_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            tenantId = request.headers.get("x-tenantId")
            if tenantId is None:
                raise ApiException(message='Tenant required',name='TENANT_INVALID', status_code=400)
            return current_app.ensure_sync(fn)(*args, **kwargs)

        return decorator

    return wrapper