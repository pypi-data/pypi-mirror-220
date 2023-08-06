# ========================================
from typing import Any, List
from sqlalchemy import and_, asc, desc, or_, select
import sqlalchemy as sa


class app_db_utils():
    # ========================================
    @staticmethod
    def orderBys(model: Any, orderBys=[]):
        resultOrderBy = []
        for orderBy in orderBys:
            if str(orderBy['order']).upper == 'ASC':
                resultOrderBy.append(
                    asc(getattr(model, orderBy['field'], None)))
            if orderBy['order'] == 'DESC':
                resultOrderBy.append(
                    desc(getattr(model, orderBy['field'], None)))

        return resultOrderBy
    # ========================================

    @staticmethod
    def filters(model_base: Any, model: Any, filters=[]):
        resultFilterAnd = []
        resultFilterOr = []
        resultGlobal = []

        # ====================
        for filter in filters:
            criteria = False

            # ====================
            filterValue = filter['value']
            if str(filterValue)[0:1] == '[' and filter['group'] == "and":
                # ====================
                criteria = app_db_utils.get_criteria_model_value(
                    model_base, model, filter['field'], filterValue)

            elif filter['operator'] == "eq" and filter['group'] == "and":
                # ====================
                criteria = getattr(
                    model, filter['field'], None) == filterValue
            elif (filter['operator'] == "like" or filter['operator'] == "ilike") and filter['group'] == "and":
                # ====================
                criteria = getattr(model, filter['field'], None).like(
                    filterValue)
            elif filter['operator'] == "in" and filter['group'] == "and":
                # ====================
                criteria = getattr(model, filter['field'], None).in_(
                    filterValue)

            if criteria != False:
                resultFilterAnd.append(criteria)
        # ====================
        for filter in filters:
            criteria = False
            # ====================
            filterValue = filter['value']
            if str(filterValue)[0:1] == '[' and filter['group'] == "or":
                # ====================
                criteria = app_db_utils.get_criteria_model_value(
                    model_base, model, filter['field'], filterValue)

            elif filter['operator'] == "eq" and filter['group'] == "or":
                # ====================
                criteria = getattr(
                    model, filter['field'], None) == filterValue
            elif (filter['operator'] == "like" or filter['operator'] == "ilike") and filter['group'] == "or":
                # ====================
                criteria = getattr(model, filter['field'], None).like(
                    filterValue)
            elif filter['operator'] == "in" and filter['group'] == "or":
                # ====================
                criteria = getattr(model, filter['field'], None).in_(
                    filterValue)
            if criteria != False:
                resultFilterOr.append(criteria)

        # ====================
        if resultFilterAnd != []:
            resultGlobal.append(and_(*resultFilterAnd))
        if resultFilterOr != []:
            resultGlobal.append(or_(*resultFilterOr))
        return resultGlobal

    # ========================================
    @staticmethod
    def get_criteria_model_value(model_base, model, filterFieldName, filterValue):
        filterValue = str(filterValue).replace('[', '')
        filterValue = str(filterValue).replace(']', '')
        tableName = filterValue[0:filterValue.index('.')]
        # ====================
        tableValue = app_db_utils.get_class_by_table(
            model_base, tableName)
        # ====================
        fieldValue = filterValue[filterValue.index(
            '.')+1:len(filterValue)]
        # ====================
        filterValue = getattr(
            tableValue, fieldValue, None)
        # ====================
        criteria = getattr(
            model, filterFieldName, None) == filterValue

        return criteria

    # ========================================

    @staticmethod
    def relations(model_base: Any, relation_parent: Any, relations=[]):
        # ====================
        resultGlobal = []
        for rel in relations:

            table = app_db_utils.get_class_by_table(
                model_base, rel.get('table', None))
            query = select(table)
            print(rel.get('filters', None))
            filter = app_db_utils.filters(
                model_base, table, rel.get('filters', None))
            query = query.where(*filter)
            resultQuery = query.exists()
            resultGlobal.append(resultQuery)
        return resultGlobal

    # ========================================
    @staticmethod
    def get_class_by_table(model_base, table):
        resultTb = None

        for mapper in model_base.registry.mappers:
            cls = mapper.class_
            classname = cls.__name__
            if not classname.startswith('_'):
                if cls.__name__ == table:
                    resultTb = cls
                    break

        return resultTb

    # ========================================

    @staticmethod
    def db_sql_raw_list(db, sql, params=None, exp_none=False, exp_msg=None) -> List:
        cursor = db.engine.connect().exec_driver_sql(sql, params)
        result = [list(i) for i in cursor]
        if exp_none and (result is None or result == []):
            msg = exp_msg
            if exp_msg is None:
                msg = 'Error db_sql - SQL:'+sql
            raise Exception(msg)
        return result

    # ========================================

    @staticmethod
    def db_sql_raw_execute(db, sql, params=None):
        result = db.engine.connect().exec_driver_sql(sql, params)
        return result

    # ========================================

    @staticmethod
    def db_sql_model_list(db, stm, exp_none=False, exp_msg=None) -> List:
        result = db.session.scalars(stm).all()
        if exp_none and (result is None or result == []):
            msg = exp_msg
            if exp_msg is None:
                msg = 'Error db_sql - SQL:'+str(stm)
            raise Exception(msg)
        return result
