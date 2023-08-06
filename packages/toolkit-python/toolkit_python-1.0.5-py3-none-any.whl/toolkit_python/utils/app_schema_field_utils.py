from datetime import timedelta, datetime
from flask import request
from flask_jwt_extended import current_user
from marshmallow import fields

from toolkit_python.utils.app_exception_utils import ApiException

# ==============================
class fields_tenant_id(fields.Field):
    def __init__(self):
        super().__init__(required=True)

    def deserialize(self, value, attr, data, **kwargs):

        tenantid = request.headers.get("x-tenantId")

        if attr is not None in data.keys():
            raise ApiException(
                message={attr: "Tenant required in body"},
                name="TENANT_INVALID",
                status_code=400,
            )
        elif data[attr] is None or data[attr] == "":
            raise ApiException(
                message={attr: "Tenant required (1)"},
                name="TENANT_INVALID",
                status_code=400,
            )
        
        elif data[attr] != tenantid:
            raise ApiException(
                message={attr: "Tenant invalid (2)"},
                name="TENANT_INVALID",
                status_code=400,
            )

        return data[attr]

    def serialize(self, attr, obj, **kwargs):
        if type(obj) is dict:
            return obj[attr]
        else:
            return getattr(obj, attr)