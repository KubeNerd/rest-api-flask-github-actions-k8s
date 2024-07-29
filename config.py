import os


class DevConfig:
    MONGODB_SETTINGS = {
        "db": os.getenv("DATABASE_NAME"),
        "host": os.getenv("DATABASE_HOST"),
        "username": os.getenv("DATABASE_USER"),
        "password": os.getenv("DATABASE_PASSWORD"),
        "port": 27017,
    }


class MockConfig:
    MONGODB_SETTINGS = {
        "db": "users",
        "host": "mongomock://localhost",
    }
