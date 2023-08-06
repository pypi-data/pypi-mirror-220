import re
from . import db
import sql_holder as holder
from support import get_batch_args, SqlAction
from log_support import logger, sql_id_log, page_sql_id_log


def init_db(user='root', password='', database='test', host='127.0.0.1', port=3306, show_sql=False, mapper_path='mapper', **kwargs):
    holder.load_mapper(mapper_path)
    db.init_db(user, password, database, host, port, show_sql, **kwargs)


def insert(table: str, **kwargs):
    """
    Insert data into table, return effect rowcount.
    :param table: table name
    :param kwargs: {'name': '张三', 'age': 20}
    return: Effect rowcount
    """
    return db.insert(table, **kwargs)


def save(table: str, **kwargs):
    """
    Insert data into table, return primary key.
    :param table: table name
    :param kwargs: {'name': '张三', 'age': 20}
    :return: Primary key
    """
    return db.save(table, **kwargs)


def mapper_save(sql_id: str, *args, **kwargs):
    """
    Execute insert SQL, return primary key.
    :return: Primary key
    """
    sql_id_log('dbx.mapper_save', sql_id, *args, **kwargs)
    sql_model = holder.get_sql_model(sql_id)
    pk_seq = sql_model.pk_seq
    if 'pk_seq' in kwargs:
        pk_seq = kwargs.pop('pk_seq')
    sql, args = holder.do_get_sql(sql_model, False, None, *args, **kwargs)
    assert SqlAction.INSERT.value in sql.lower(), 'Only insert sql can return primary key.'
    if not pk_seq:
        table = re.search('(?<=into )\w+', sql.lower())
        pk_seq = "{}_id_seq".format(table.group())
        logger.warning("Exec func 'mysqlx.dbx.mapper_save': 'pk_seq' is None, will use default '{}'.".format(pk_seq))

    return db.do_save(pk_seq, sql, *args)


def execute(sql_id: str, *args, **kwargs):
    """
    Execute SQL.
    sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('dbx.execute', sql_id, *args, **kwargs)
    sql, args = holder.get_sql(sql_id, *args, **kwargs)
    return db.do_execute(sql, *args)


def batch_insert(table: str, *args):
    """
    Batch insert
    :param table: table name
    :param args: All number must have same key. [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    return db.batch_insert(table, *args)


def batch_execute(sql_id: str, *args):
    """
    Batch execute
    sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
         INSERT INTO person(name, age) VALUES(:name,:age)  -->  args: [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    logger.debug("Exec func 'mysqlx.dbx.%s' \n\t sql_id: '%s' \n\t args: %s" % ('batch_execute', sql_id, args))
    args = get_batch_args(*args)
    sql, _ = holder.do_get_sql(holder.get_sql_model(sql_id), True, None, *args)
    return db.batch_execute(sql, *args)


# ----------------------------------------------------------Query function------------------------------------------------------------------
def get(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' behind the sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('get', sql_id, *args, **kwargs)
    sql, args = holder.get_sql(sql_id, *args, **kwargs)
    return db.do_get(sql, *args)


def query(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('query', sql_id, *args, **kwargs)
    sql, args = holder.get_sql(sql_id, *args, **kwargs)
    return db.do_query(sql, *args)


def query_one(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(dict). Automatically add 'limit ?' behind the sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('query_one', sql_id, *args, **kwargs)
    sql, args = holder.get_sql(sql_id, *args, **kwargs)
    return db.do_query_one(sql, *args)


def select(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('select', sql_id, *args, **kwargs)
    sql, args = holder.get_sql(sql_id, *args, **kwargs)
    return db.do_select(sql, *args)


def select_one(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(tuple). Automatically add 'limit ?' behind the sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('select_one', sql_id, *args, **kwargs)
    sql, args = holder.get_sql(sql_id, *args, **kwargs)
    return db.do_select_one(sql, *args)


def query_page(sql_id: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_sql_id_log('query_page', sql_id, page_num, page_size, *args, **kwargs)
    sql, args = holder.get_sql(sql_id, *args, **kwargs)
    return db.do_query_page(sql, page_num, page_size, *args)


def select_page(sql_id: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_sql_id_log('select_page', sql_id, page_num, page_size, *args, **kwargs)
    sql, args = holder.get_sql(sql_id, *args, **kwargs)
    return db.do_select_page(sql, page_num, page_size, *args)


def get_connection():
    return db.get_connection()

