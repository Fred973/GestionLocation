from app.constant import secret_key, mysql_sqalchemy


class Config:
    SQLALCHEMY_DATABASE_URI = mysql_sqalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = True   # /home/fred/Dropbox/Divers Frederic
                                            # Menoud/dev/noctuelle/venv/lib/python3.8/site-packages/flask_sqlalchemy/__init__.py:872: FSADeprecationWarning:
                                            # SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to
                                            # True or False to suppress this warning. warnings.warn(FSADeprecationWarning(
    SECRET_KEY = secret_key
    