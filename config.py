from os import environ

class BaseConfig:
    SECRET_KEY = "make-this-key-powerfull"
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL") or "sqlite:///dev.db"
    SUPPORTED_LANGUAGES = {'en': 'English', 'pt': 'Portuguese'}
    BABEL_DEFAULT_LOCALE = 'pt'