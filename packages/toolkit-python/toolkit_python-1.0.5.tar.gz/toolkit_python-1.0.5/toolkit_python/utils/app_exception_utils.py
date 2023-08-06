# ========================================
class ApiException(Exception):
    status_code = 400

    # ====================================

    def __init__(self, message, name, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.name = name

    # ====================================

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['name'] = self.name
        rv['status'] = 'ERROR'
        return rv
