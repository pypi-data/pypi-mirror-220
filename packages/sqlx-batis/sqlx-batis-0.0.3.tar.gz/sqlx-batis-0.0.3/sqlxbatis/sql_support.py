import re
import sqlexec
from jinja2 import Template
from .support import SqlAction
from .log_support import logger
from functools import lru_cache
from .support import MapperError
from . import sql_holder as holder, Engin
from .constant import CACHE_SIZE, LIMIT_1, DYNAMIC_REGEX
from sqlexec.sql_support import get_select_key, get_engin, require_limit, get_named_sql_args

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


def is_dynamic_sql(sql: str):
    return re.search(DYNAMIC_REGEX, sql)


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


def limit_one_sql_args(sql: str, *args):
    if require_limit(sql):
        return '{} LIMIT ?'.format(sql), [*args, LIMIT_1]
    return sql, args


def do_save(sql_model, batch, param_names, *args, **kwargs):
    assert SqlAction.INSERT.value == sql_model.action, 'Only insert sql can return primary key.'
    sql, args = holder.do_get_sql(sql_model, batch, param_names, *args, **kwargs)
    select_key = sql_model.select_key
    pk_seq = sql_model.pk_seq
    return  do_save0(select_key, pk_seq, sql, *args)


def do_save0(select_key, pk_seq, sql, *args):
    if select_key:
        return sqlexec.save_sql(select_key, sql, *args)

    if get_engin() == Engin.MySQL:
        return sqlexec.save_sql(get_select_key(), sql, *args)
    if get_engin() == Engin.PostgreSQL:
        if not pk_seq:
            table = re.search('(?<=into )\w+', sql, re.I)
            pk_seq = "{}_id_seq".format(table.group())
            logger.warning("Exec func 'mysqlx.dbx.mapper_save': 'pk_seq' is None, will use default '{}'.".format(pk_seq))
        return sqlexec.save_sql(get_select_key(pk_seq), sql, *args)

    raise
