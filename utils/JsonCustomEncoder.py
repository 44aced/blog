import json
from django.core.exceptions import ValidationError
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field,ValidationError):
            return {'code':field.code,'message':field.message}
        else:
            return json.JSONEncoder.default(self,field)