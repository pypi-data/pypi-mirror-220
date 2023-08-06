import re
from typing import Sequence
from jinja2 import Template
from functools import lru_cache
from .log_support import logger
from .support import MapperError
from .constant import LIMIT_1, NAMED_REGEX, DYNAMIC_REGEX, CACHE_SIZE

_SHOW_SQL = False


def set_show_sql(show_sq: bool):
    global _SHOW_SQL
    _SHOW_SQL = show_sq


def before_execute(function: str, sql: str, *args):
    global _SHOW_SQL
    if _SHOW_SQL:
        logger.info("Exec func 'mysqlx.db.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
    return sql.replace('?', '%s')


def before_select(function: str, sql: str, *args):
    global _SHOW_SQL
    if _SHOW_SQL:
        logger.info("Exec func 'mysqlx.db.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))

    if '%' in sql and 'like' in sql.lower():
        sql = sql.replace('%', '%%').replace('%%%%', '%%')

    return sql.replace('?', '%s')


def insert_sql_args(table: str, **kwargs):
    cols, args = zip(*kwargs.items())
    sql = _create_insert_sql(table, cols)
    return sql, args


def batch_insert_sql_args(table: str, *args):
    args = get_batch_args(*args)
    args = [zip(*arg.items()) for arg in args]  # [(cols, args)]
    cols, args = zip(*args)  # (cols), (args)
    sql = _create_insert_sql(table, cols[0])
    return sql, args


def batch_named_sql_args(sql: str, *args):
    args = get_batch_args(*args)
    args = [get_named_args(sql, **arg) for arg in args]
    sql = get_named_sql(sql)
    return sql, args


@lru_cache(maxsize=CACHE_SIZE)
def _create_insert_sql(table: str, cols: Sequence[str]):
    columns, placeholders = zip(*[('{}'.format(col), '?') for col in cols])
    return 'INSERT INTO {}({}) VALUES({})'.format(table, ','.join(columns), ','.join(placeholders))


def page_sql_args(sql: str, page_num=1, page_size=10, *args):
    start = (page_num - 1) * page_size
    args = [*args, page_size, start]
    if _require_limit(sql):
        sql = '{} LIMIT ? OFFSET ?'.format(sql)
    return sql, args


def limit_one_sql_args(sql: str, *args):
    if _require_limit(sql):
        return '{} LIMIT ?'.format(sql), [*args, LIMIT_1]

    return sql, args


def _require_limit(sql: str):
    lower_sql = sql.lower()
    if 'limit' not in lower_sql:
        return True

    idx = lower_sql.rindex('limit')
    if idx > 0 and ')' in lower_sql[idx:]:
        return True

    return False


def get_batch_args(*args):
    return args[0] if isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], Sequence) else args


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


def get_named_sql_args(sql: str, **kwargs):
    args = get_named_args(sql, **kwargs)
    return get_named_sql(sql), args


@lru_cache(maxsize=CACHE_SIZE)
def get_named_sql(sql: str):
    return re.sub(NAMED_REGEX, '?', sql)


def get_named_args(sql: str, **kwargs):
    return [kwargs[r[1:]] for r in re.findall(NAMED_REGEX, sql)]
