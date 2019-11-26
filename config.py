from os import environ

class BaseConfig:
    SECRET_KEY = "247Z3D80Fm5qXMzteOJEguXnr0yZUaPutSbVKjmS"
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL") or "sqlite:///data/dev.db"