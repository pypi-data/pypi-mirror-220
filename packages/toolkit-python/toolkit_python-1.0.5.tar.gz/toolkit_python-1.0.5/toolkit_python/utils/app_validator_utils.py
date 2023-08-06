from marshmallow.validate import Validator, _T
from sqlalchemy.orm import class_mapper
from toolkit_python.utils.app_exception_utils import ApiException
from flask import current_app


# ==============================


class app_validator_utils:
    @staticmethod
    def valid_unique_fields(obj, model, unique_fields, db):
        filters = []
        filters_msg = ""
        # Busca colunas para serem incluidas como filtro unique
        for col in unique_fields:
            col_mapper = class_mapper(model)
            if not hasattr(col_mapper.columns, col):
                continue
            filters.append(col_mapper.columns[col].__eq__(getattr(obj, col)))
            filters_msg += (
                col_mapper.columns[col].name + "=" +
                str(getattr(obj, col)) + ","
            )

        filters_msg = filters_msg[0: (len(filters_msg) - 1)]

        # Busca registro com ID diferente para validar unique
        filters.append(col_mapper.columns["id"].__ne__(getattr(obj, "id")))

        objUnique = db.session.query(model).filter(*filters).first()

        if objUnique is not None:
            return {"unique": True, "message": filters_msg}
        else:
            return {"unique": False, "message": None}
