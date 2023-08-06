from sqlexec.sql_support import logger

def sql_id_log(function: str, sql_id: str, *args, **kwargs):
    logger.debug("Exec func 'sqlx-batis.%s', sql_id: %s, args: %s, kwargs: %s" % (function, sql_id.strip(), args, kwargs))


def page_sql_id_log(function: str, sql_id: str, page_num, page_size, *args, **kwargs):
    logger.debug("Exec func 'sqlx-batis.%s', page_num: %d, page_size: %d, sql_id: %s, args: %s, kwargs: %s" % (function, page_num, page_size, sql_id, args, kwargs))

