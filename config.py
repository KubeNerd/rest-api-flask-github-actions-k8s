import os


class DevConfig:
    MONGODB_SETTINGS = {
        "db": "users",
        "host": "mongodb",
        "username": os.getenv("DATABASE_USER"),
        "password": os.getenv("DATABASE_PASSWORD"),
        "port": 27017,
    }


class MockConfig:
    MONGODB_SETTINGS = {
        "db": "users",
        "host": "mongomock://localhost",
    }
