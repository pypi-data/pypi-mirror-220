import re
from jinja2 import Template
from functools import lru_cache
from .support import MapperError
from .constant import LIMIT_1, DYNAMIC_REGEX, CACHE_SIZE
from sqlexec.sql_support import require_limit, get_named_args, get_named_sql

def simple_sql(sql: str, *args, **kwargs):
    return get_named_sql_args(sql, **kwargs) if kwargs else (sql, args)


def dynamic_sql(sql: str, *args, **kwargs):
    sql_type = _get_sql_type(sql)
    if sql_type >= 1 and not kwargs:
        raise MapperError("Parameter 'kwargs' must not be empty when named mapping sql.")
    if sql_type == 0:
        return sql, args
    if sql_type == 1:
        sql = Template(sql).render(**kwargs)
    return get_named_sql_args(sql, **kwargs)


def limit_one_sql_args(sql: str, *args):
    if require_limit(sql):
        return '{} LIMIT ?'.format(sql), [*args, LIMIT_1]
    return sql, args


def is_dynamic_sql(sql: str):
    return re.search(DYNAMIC_REGEX, sql)


def get_named_sql_args(sql: str, **kwargs):
    args = get_named_args(sql, **kwargs)
    return get_named_sql(sql), args


@lru_cache(maxsize=2*CACHE_SIZE)
def _get_sql_type(sql: str):
    """
    :return: 0: placeholder, 1: dynamic, 2: named mapping
    """
    if is_dynamic_sql(sql):
        return 1
    if ':' in sql:
        return 2
    return 0

