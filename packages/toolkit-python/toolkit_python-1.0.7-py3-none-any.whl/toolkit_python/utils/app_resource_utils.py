import json
from flask import request
from toolkit_python.utils.app_exception_utils import ApiException
# ========================================


class app_resource_utils:
    # ========================================
    @staticmethod
    def req_param():
        filter = request.args.get("filter", default=None)
        if filter is not None:
            filter = json.loads(filter)

        return filter
    # ========================================

    @staticmethod
    def req_tenant_id():
        tenantId = request.headers.get("x-tenantId", default=None)
        if tenantId is None:
            raise ApiException(
                message='Tenant invalid (Header)', name='TENANT_INVALID', status_code=400)
        return tenantId

    # ========================================
    @staticmethod
    def req_body():
        body = request.get_json()
        return body
