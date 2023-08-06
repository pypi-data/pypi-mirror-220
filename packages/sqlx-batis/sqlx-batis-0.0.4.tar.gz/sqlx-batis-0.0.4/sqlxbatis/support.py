from enum import Enum
from .import DBError


class MapperError(DBError):
    pass


class SqlAction(Enum):
    CALL = 'call'
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'
    SELECT = 'select'
