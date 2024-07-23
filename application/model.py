from .db import db


class UserModel(db.Document):
    cpf = db.StringField(max_length=200, unique=True)
    email = db.StringField(max_length=200, required=True)
    first_name = db.StringField(max_length=200, required=True)
    last_name = db.StringField(max_length=200, required=True)
    birth_date = db.DateTimeField(required=True)
