import sqlexec
from . import sql_support, Engin
from sqlexec.constant import MAPPER_PATH
from .log_support import sql_log, page_log, insert_log, do_sql_log

# Don't remove. Import for not repetitive implementation
from sqlexec import(insert, save, save_sql, batch_insert, batch_execute)


def init_db(user='root', password='', database='test', host='127.0.0.1', port=3306, engin=Engin.MySQL, pool_size=2, show_sql=False, **kwargs):
    if MAPPER_PATH in kwargs:
        from .sql_holder import load_mapper
        load_mapper(kwargs.pop(MAPPER_PATH))
    sqlexec.init_db(user=user, password=password, database=database, host=host, port=port, engin=engin, pool_size=pool_size, show_sql=show_sql, **kwargs)


# ----------------------------------------------------------Update function------------------------------------------------------------------
def execute(sql: str, *args, **kwargs):
    """
    Execute SQL.
    sql: INSERT INTO user(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO user(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('execute', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_execute(sql, *args)


# ----------------------------------------------------------Query function------------------------------------------------------------------
def get(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' after sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('get', sql, *args, **kwargs)
    global _DB_CTX
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_get(sql, *args)


def query(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('query', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_query(sql, *args)


def query_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(dict). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('query_one', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_query_one(sql, *args)


def select(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('select', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_select(sql, *args)


def select_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(tuple). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('select_one', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_select_one(sql, *args)


def query_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_log('query_page', sql, page_num, page_size, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_query_page(sql, page_num, page_size, *args)


def select_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_log('select_page', sql, page_num, page_size, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_select_page(sql, page_num, page_size, *args)


# ----------------------------------------------------------Do function------------------------------------------------------------------
def do_execute(sql: str, *args):
    """
    Execute sql return effect rowcount
    sql: insert into user(name, age) values(?, ?)  -->  args: ('张三', 20)
    """
    return sqlexec.execute(sql, *args)


def do_get(sql: str, *args):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' behind the sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    do_sql_log('do_get', sql, *args)
    sql, args = sql_support.limit_one_sql_args(sql, *args)
    return sqlexec.get(sql, *args)


def do_query(sql: str, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    return sqlexec.query(sql, *args)


def do_query_one(sql: str, *args):
    """
    execute select SQL and return unique result(dict). Automatically add 'limit ?' behind the sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    do_sql_log('do_query_one', sql, *args)
    sql, args = sql_support.limit_one_sql_args(sql, *args)
    return sqlexec.query_one(sql, *args)


def do_select(sql: str, *args):
    """
    execute select SQL and return unique result or list results(tuple).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    return sqlexec.select(sql, *args)


def do_select_one(sql: str, *args):
    """
    Execute select SQL and return unique result(tuple). Automatically add 'limit ?' behind the sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    do_sql_log('do_select_one', sql, *args)
    sql, args = sql_support.limit_one_sql_args(sql, *args)
    return sqlexec.select_one(sql, *args)


def do_query_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    return sqlexec.query_page(sql, page_num, page_size, *args)


def do_select_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    return sqlexec.select_page(sql, page_num, page_size, *args)

