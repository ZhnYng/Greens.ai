from application.utils.QueryUtils import QueryUtils
from application.models import Entry
from flask import Response
from flask_jwt_extended import decode_token

class Authorization:
    def model_auth(self, model, object_id, jwt_token):
        decoded_jwt_token = decode_token(jwt_token)
        query_utils = QueryUtils()

        # Authorization
        this_entry = query_utils.get_entries_where(
            model, condition=model.id == object_id
        )[0]
        # Checks if current logged in user owns the entry
        if int(this_entry["user_id"]) != int(decoded_jwt_token['sub']):
            return "Not Authorized"
        else:
            return "Authorized"