# user-service/app/models/__init__.py

from sqlalchemy.ext.declarative import declarative_base

# Base class mà tất cả các models của service này sẽ kế thừa
Base = declarative_base()