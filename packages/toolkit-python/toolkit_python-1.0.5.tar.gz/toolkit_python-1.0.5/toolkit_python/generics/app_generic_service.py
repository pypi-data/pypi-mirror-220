from typing import Any
from sqlalchemy import Table, delete, select, MetaData
from sqlalchemy.orm import Session
from toolkit_python.utils.app_db_utils import app_db_utils
from toolkit_python.utils.app_validator_utils import app_validator_utils
from toolkit_python.utils.app_exception_utils import ApiException

# ========================================


class app_generic_service:
    db_session: Any
    # ========================================

    def __init__(self, db_session=None):
        self.db_session = db_session

     # ========================================

    def list_generic(self,
                     model_base: Any,
                     model: Any,
                     schema: Any,
                     column="*",
                     column_exclude=[],
                     filters=[],
                     pagination=None,
                     fieldsOrderDefault=[],
                     relations=[]):
        # ====================
        paginationAux = pagination
        if pagination is None:
            paginationAux = {"page": 1, "size": 10}
        # ====================
        dbSession = Session(self.db.engine)
        query = select(model)
        # ====================
        filter = app_db_utils.filters(model_base, model, filters)
        query = query.where(*filter)
        # ====================
        relation = app_db_utils.relations(model_base, model, relations)
        query = query.where(*relation)
        # ====================
        orderBy = app_db_utils.orderBys(
            model, fieldsOrderDefault)
        query = query.order_by(*orderBy)
        # ====================
        query = query.limit(paginationAux["size"]).offset(
            (paginationAux['page'] - 1) * paginationAux["size"])
        # ====================
        result = dbSession.scalars(query).all()
        # ====================
        resultJson = schema(exclude=column_exclude, many=True).dump(result)

        result = {
            "total": result.count,
            "data": resultJson,
            "page": paginationAux['page'],
            "rows": paginationAux["size"],
        }

        # ====================
        return resultJson

    # ==============================
    def save_generic(self, model, schema, obj, unique_fields=[], column_exclude=[]):
        if unique_fields != []:
            objUnique = app_validator_utils.valid_unique_fields(
                obj, model, unique_fields, self.db
            )
            if objUnique["unique"]:
                raise ApiException(
                    message="Record exists, is unique columns [{}]".format(
                        objUnique["message"]
                    ),
                    name='VALIDATION_UNIQUE_ERROR',
                    status_code=400,
                )

        self.db_session.add(obj)
        self.db_session.flush()
        resultJson = schema(exclude=column_exclude).dump(obj)
        return resultJson

     # ========================================

    def delete_generic(self,
                     model_base: Any,
                     model: Any,
                     filters=[]):
        # ====================
        query = delete(model)
        # ====================
        filter = app_db_utils.filters(model_base, model, filters)
        query = query.where(*filter)
        result = self.db_session.execute(query,execution_options={"autoflush":False})
        # ====================
        return result