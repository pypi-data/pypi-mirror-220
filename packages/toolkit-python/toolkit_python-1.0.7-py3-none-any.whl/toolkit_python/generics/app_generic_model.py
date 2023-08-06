from datetime import datetime
import uuid
from sqlalchemy import TIMESTAMP, Column, String
from flask_jwt_extended import get_current_user

# ========================================


def gen_model_uuid():
    return str(uuid.uuid4())

# ========================================


def get_model_login():
    try:
        user = get_current_user()
        return user[0].login
    except Exception as e:
        return "anonymus"

# ========================================


def get_model_now():
    return datetime.now()

# ========================================


class app_generic_model(object):
    pass
