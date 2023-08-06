import functools
from . import sql_support
from .constant import MAPPER_PATH
from .log_support import logger, sql_log, page_log, insert_log, do_sql_log, do_page_log
from .support import DBCtx, ConnectionCtx, Dict, MultiColumnsError, TransactionCtx, try_commit, DBError, DB_LOCK

_DB_CTX = None


def init_db(user='root', password='', database='test', host='127.0.0.1', port=3306, show_sql=False, **kwargs):
    kwargs['user'] = user
    kwargs['password'] = password
    kwargs['database'] = database
    kwargs['host'] = host
    kwargs['port'] = port
    sql_support.set_show_sql(show_sql)

    if 'debug' in kwargs:
        if kwargs.pop('debug'):
            from logging import DEBUG
            logger.setLevel(DEBUG)

    _init_db(**kwargs)


def _init_db(**kwargs):
    global _DB_CTX
    from psycopg2 import connect
    with DB_LOCK:
        if _DB_CTX is not None:
            raise DBError('DB is already initialized.')

        if MAPPER_PATH in kwargs:
            from .sql_holder import load_mapper
            load_mapper(kwargs.pop(MAPPER_PATH))

        _DB_CTX = DBCtx(connect=lambda: connect(**kwargs))
        logger.info('Init db engine <%s> ok without connection pool.' % hex(id(_DB_CTX)))


def connection():
    """
    Return _ConnectionCtx object that can be used by 'with' statement:
    with connection():
        pass
    """
    global _DB_CTX
    return ConnectionCtx(_DB_CTX)


def with_connection(func):
    """
    Decorator for reuse connection.
    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
    """

    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with ConnectionCtx(_DB_CTX):
            return func(*args, **kw)

    return _wrapper


def transaction():
    """
    Create a transaction object so can use with statement:
    with transaction():
        pass
    with transaction():
         insert(...)
         update(... )
    """
    global _DB_CTX
    return TransactionCtx(_DB_CTX)


def with_transaction(func):
    """
    A decorator that makes function around transaction.
    @with_transaction
    def update_profile(id, name, rollback):
         u = dict(id=id, name=name, email='%s@test.org' % name, passwd=name, last_modified=time.time())
         insert('person', **u)
         r = update('update person set passwd=? where id=?', name.upper(), id)
    """
    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with TransactionCtx(_DB_CTX):
            return func(*args, **kw)

    return _wrapper


# ----------------------------------------------------------Update function------------------------------------------------------------------
def insert(table: str, **kwargs):
    """
    Insert data into table, return effect rowcount.
    :param table: table name
    :param kwargs: name='张三', age=20}
    return: Effect rowcount
    """
    insert_log('insert', table, **kwargs)
    sql, args = sql_support.insert_sql_args(table.strip(), **kwargs)
    return do_execute(sql, *args)


def save(table: str, **kwargs):
    """
    Insert data into table, return primary key.
    Default primary key sequnece is 'table_id_seq', you can use 'pk_seq' define it
    :param table: table
    :param kwargs: name='张三', age=20
    :return: Primary key
    """
    insert_log('save', table, **kwargs)
    if 'pk_seq' in kwargs:
        pk_seq = kwargs.pop('pk_seq')
    else:
        pk_seq = "{}_id_seq".format(table)
    sql, args = sql_support.insert_sql_args(table.strip(), **kwargs)
    return do_save(pk_seq, sql, *args)


@with_connection
def do_save(pk_seq: str, sql: str, *args):
    """
    Insert data into table, return primary key.
    :param pk_seq: primary key sequnece
    :param sql: table
    :param args:
    :return: Primary key
    """
    global _DB_CTX
    cursor = None
    logger.debug("Exec func 'mysqlx.db.%s': pk_seq: '%s'\n\tsql: '%s'\n\targs: %s" % ('do_save', pk_seq, sql, args))
    sql = sql_support.before_execute('do_save', sql, *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        cursor.execute("SELECT currval('{}')".format(pk_seq))
        result = cursor.fetchone()
        try_commit(_DB_CTX)
        return result[0]
    finally:
        if cursor:
            cursor.close()


def execute(sql: str, *args, **kwargs):
    """
    Execute SQL.
    sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('db.execute', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_execute(sql, *args)


def batch_insert(table: str, *args):
    """
    Batch insert
    :param table: table name
    :param args: All number must have same key. [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    logger.debug("Exec func 'mysqlx.db.%s' \n\t Table: '%s', args: %s" % ('batch_insert', table, args))
    assert len(args) > 0, 'args must not be empty.'
    sql, args = sql_support.batch_insert_sql_args(table, *args)
    return batch_execute(sql, *args)


def batch_execute(sql: str, *args):
    """
    Batch execute
    :param sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
                INSERT INTO person(name, age) VALUES(:name,:age)  -->  args: [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :param args: All number must have same size.
    :return: Effect row count
    """
    logger.debug("Exec func 'mysqlx.db.%s' \n\t sql: '%s' \n\t args: %s" % ('batch_execute', sql, args))
    assert len(args) > 0, 'args must not be empty.'
    if isinstance(args[0], dict):
        sql, args = sql_support.batch_named_sql_args(sql, *args)

    return do_batch_execute(sql, *args)


# ----------------------------------------------------------Query function------------------------------------------------------------------
def get(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' after sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('get', sql, *args, **kwargs)
    global _DB_CTX
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_get(sql, *args)


def query(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('query', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_query(sql, *args)


def query_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(dict). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('query_one', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_query_one(sql, *args)


def select(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('select', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_select(sql, *args)


def select_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(tuple). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_log('select_one', sql, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_select_one(sql, *args)


def query_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_log('query_page', sql, page_num, page_size, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_query_page(sql, page_num, page_size, *args)


def select_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_log('select_page', sql, page_num, page_size, *args, **kwargs)
    sql, args = sql_support.dynamic_sql(sql, *args, **kwargs)
    return do_select_page(sql, page_num, page_size, *args)


# ----------------------------------------------------------Do function------------------------------------------------------------------
@with_connection
def do_execute(sql: str, *args):
    """
    Execute sql return effect rowcount
    sql: insert into person(name, age) values(?, ?)  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_execute('do_execute', sql.strip(), *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_batch_execute(sql: str, *args):
    """
    Batch execute sql return effect rowcount
    :param sql: insert into person(name, age) values(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
    :param args: All number must have same size.
    :return: Effect rowcount
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_execute('do_batch_execute', sql.strip(), *args)
    args = sql_support.get_batch_args(*args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.executemany(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()


def do_get(sql: str, *args):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' behind the sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    do_sql_log('do_get', sql, *args)
    sql, args = sql_support.limit_one_sql_args(sql, *args)
    return do_get_limit(sql, *args)


def do_get_limit(sql: str, *args):
    """
    Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    do_sql_log('do_get_with_limit', sql, *args)
    result = do_select_one_limit(sql, *args)
    if result:
        if len(result) == 1:
            return result[0]
        msg = "Exec func 'mysqlx.db.%s' expect only one column but %d." % ('do_get_limit', len(result))
        logger.error('%s  \n\t sql: %s \n\t args: %s' % (msg, sql, args))
        raise MultiColumnsError(msg)
    return None


@with_connection
def do_query(sql: str, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_select('do_query', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        results = cursor.fetchall()
        if results and cursor.description:
            names = [x[0] for x in cursor.description]
            return [Dict(names, x) for x in results]
        else:
            return results
    finally:
        if cursor:
            cursor.close()


def do_query_one(sql: str, *args):
    """
    execute select SQL and return unique result(dict). Automatically add 'limit ?' behind the sql statement if not.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    do_sql_log('do_query_one', sql, *args)
    sql, args = sql_support.limit_one_sql_args(sql, *args)
    return do_query_one_limit(sql, *args)


@with_connection
def do_query_one_limit(sql: str, *args):
    """
    execute select SQL and return unique result(dict), SQL contain 'limit'.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_select('do_query_one_limit', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        if result and cursor.description:
            names = [x[0] for x in cursor.description]
            return Dict(names, result)
        return result
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_select(sql: str, *args):
    """
    execute select SQL and return unique result or list results(tuple).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_select('do_select', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()


def do_select_one(sql: str, *args):
    """
    Execute select SQL and return unique result(tuple). Automatically add 'limit ?' behind the sql statement if not.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    do_sql_log('do_select_one', sql, *args)
    sql, args = sql_support.limit_one_sql_args(sql, *args)
    return do_select_one_limit(sql, *args)


@with_connection
def do_select_one_limit(sql: str, *args):
    """
    Execute select SQL and return unique result(tuple), SQL contain 'limit'.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_select('do_select_one_limit', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()


def do_query_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    do_page_log('do_query_page', sql, page_num, page_size, args)
    sql, args = sql_support.page_sql_args(sql, page_num, page_size, *args)
    return do_query(sql, *args)


def do_select_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    do_page_log('do_select_page', sql, page_num, page_size, args)
    sql, args = sql_support.page_sql_args(sql, page_num, page_size, *args)
    return do_select(sql, *args)


def get_connection():
    global _DB_CTX
    if _DB_CTX.is_not_init():
        _DB_CTX.init()
    return _DB_CTX.connection


def prepare(prepared=True):
    global _DB_CTX
    _DB_CTX.prepared = prepared
