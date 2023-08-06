import re
from .constant import LIMIT_1, DYNAMIC_REGEX
from sqlexec.sql_support import require_limit, get_named_args, get_named_sql

def simple_sql(sql: str, *args, **kwargs):
    return get_named_sql_args(sql, **kwargs) if kwargs else (sql, args)


def limit_one_sql_args(sql: str, *args):
    if require_limit(sql):
        return '{} LIMIT ?'.format(sql), [*args, LIMIT_1]
    return sql, args


def is_dynamic_sql(sql: str):
    return re.search(DYNAMIC_REGEX, sql)


def get_named_sql_args(sql: str, **kwargs):
    args = get_named_args(sql, **kwargs)
    return get_named_sql(sql), args

