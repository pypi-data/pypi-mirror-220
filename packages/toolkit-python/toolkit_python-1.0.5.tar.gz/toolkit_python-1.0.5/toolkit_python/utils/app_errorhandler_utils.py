from datetime import datetime
import logging
import traceback
from flask import json, Response, jsonify
from werkzeug.exceptions import HTTPException
from marshmallow.exceptions import ValidationError
from toolkit_python.utils.app_exception_utils import ApiException


def errorhandler(e):
    try:
        if isinstance(e, HTTPException):

            logging.error(e.name+' - '+e.description)
            response = e.get_response()
            response.data = json.dumps({
                "datetime": datetime.now().strftime('%d/%m/%Y  %H:%M:%S.%f'),
                "code": e.code,
                "name": e.name,
                "message": e.description,
            })
            response.content_type = "application/json"
            return response

        elif isinstance(e, ApiException):
            response = jsonify(e.to_dict())
            response.status_code = e.status_code
            return response
        elif isinstance(e, ValidationError):
            response = Response()
            response.data = json.dumps({
                "datetime": datetime.now().strftime('%d/%m/%Y  %H:%M:%S.%f'),
                "code": 400,
                "name": 'VALIDATION_ERROR',
                "message": e.messages
            })
            response.content_type = "application/json"
            response.status_code = 400
            return response

        else:
            logging.error('Internal Error - '+traceback.format_exc())
            description = str(traceback.format_exc())
            description = description.replace('\n', ' ')
            description = description.replace('  ', ' ')
            name = 'Internal Error'
            # ===============
            index1 = description.find('RuntimeError:')

            # ===============
            if index1 < 0:
                index1 = description.find('ValueError:')

            descriptionStart = int(index1)
            descriptionEnd = int(len(description)-descriptionStart)
            description = description[-descriptionEnd:]
            response = Response()
            response.status_code = 500

           # ===============
            if index1 < 0:
                index1 = description.find('ForeignKeyViolation:')
                if index1 > 0:
                    description = "Registry with invalid dependencies, operation not allowed"
                    name = 'VALIDATION_DEPS_ERROR'
            # ===============
            if index1 < 0:
                index1 = description.find('NotNullViolation:')
                if index1 > 0:
                    description = "NotNull constraint violate"
                    name = 'VALIDATION_NOTNULL_ERROR'

            # ===============
            if index1 < 0:
                index1 = description.find('sqlalchemy.exc.IntegrityError:')
                if index1 > 0:
                    description = "Integrity constraint violate"
                    name = 'VALIDATION_INTEGRITY_ERROR'

            # ===============
            if index1 < 0:
                index1 = description.find(
                    'duplicate key value violates unique constraint')
                if index1 > 0:
                    description = "Unique constraint violate"
                    name = 'VALIDATION_UNIQUE_ERROR'

            # ===============
            if index1 < 0:
                index1 = description.find('Failed to decode JSON object')
                if index1 > 0:
                    description = "Json body invalid"

            # ===============
            if index1 < 0:
                index1 = description.find(
                    'jinja2.exceptions.TemplateNotFound:')
                if index1 > 0:
                    description = "Template not found"

            # ===============
            if index1 < 0:
                index1 = description.find(
                    ' werkzeug.exceptions.NotFound:')
                if index1 > 0:
                    description = "Data or Page not found"
                    response.status_code = 404
                    name = 'URL_NOT_FOUND'

            response.data = json.dumps({
                "datetime": datetime.now().strftime('%d/%m/%Y  %H:%M:%S.%f'),
                "code": response.status_code,
                "name": name,
                "message": description
            })
            response.content_type = "application/json"
            return response
    except Exception as e:
        response = Response()
        response.status_code = 500
        response.data = json.dumps({
            "datetime": datetime.now().strftime('%d/%m/%Y  %H:%M:%S.%f'),
            "code": response.status_code,
            "name": 'Internal Error',
            "message": str(traceback.format_exc())
        })
        response.content_type = "application/json"
        return response
