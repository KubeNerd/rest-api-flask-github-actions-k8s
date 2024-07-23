from .db import db

class UserModel(db.Document):
    __tablename__ = 'users'
    cpf = db.StringField(max_length=200, unique=True)
    email = db.StringField(max_length=200, required=True)
    first_name = db.StringField(max_length=200, required=True)
    last_name = db.StringField(max_length=200, required=True)
    birth_date = db.DateTimeField(required=True)

class Counter(db.Document):
    collection_name = db.StringField(max_length=200, unique=True, required=True)
    seq = db.IntField(required=True, default=0)


def get_next_sequence_value(collection_name):
    counter = Counter.objects(collection_name=collection_name).modify(upsert=True, new=True, inc__seq=1)
    return counter.seq

class HealthCheckModel(db.Document):
    __tablename__ = 'healthcheck'
    id = db.IntField(primary_key=True, default=lambda: get_next_sequence_value('healthcheck'))
    status = db.StringField(max_length=200, unique=False)