Usage Sample
''''''''''''

.. code:: python

   import sqlexec
   from sqlexec import Engin

   if __name__ == '__main__':
       sqlexec.init_engin(host='127.0.0.1', port='3306', person='xxx', password='xxx', database='test', show_sql=True, engin=Engin.PostgreSQL)

       select_key = "SELECT currval('person_id_seq')"
       id = sqlexec.save(select_key=select_key, table='person', name='zhangsan', age=15)
       id = sqlexec.save_sql(select_key, 'INSERT INTO person(name,age) VALUES(?,?)', 'lisi', 26)
       rowcount = sqlexec.insert(table='person', name='wangwu', age=38)

       count = sqlexec.get('select count(1) from person')
       # result: 3

       persons = sqlexec.select('select id, name, age from person')
       # result:
       # (3, 'zhangsan', 15)
       # (4, 'lisi', 26)
       # (5, 'wangwu', 38)
       
       persons = sqlexec.select_one('select id, name, age from person where name=?', 'zhangsan')
       # result:
       # (3, 'zhangsan', 15)

       persons = sqlexec.query('select id, name, age from person')
       # result:
       # {'id': 3, 'name': 'zhangsan', 'age': 15}
       # {'id': 4, 'name': 'lisi', 'age': 26}
       # {'id': 5, 'name': 'wangwu', 'age': 38}

       persons = sqlexec.query_one('select id, name, age from person where name=?', 'zhangsan')
       # result:
       # {'id': 3, 'name': 'zhangsan', 'age': 15}

       rowcount = sqlexec.execute('delete from person where id = ?', 5)
       count = sqlexec.get('select count(1) from person')
       # result: 2

Transaction
'''''''''''

.. code:: python

   from sqlexec import with_transaction, transaction

   @with_transaction
   def test_transaction():
       insert_func(....)
       update_func(....)


   def test_transaction2():
       with transaction():
           insert_func(....)
           update_func(....)


If you want to operate MySQL database like Mybatis, you may need MySqlx: https://pypi.org/project/mysqlx

If you want to operate PostgreSQL database like Mybatis, you may need PgSqlx: https://pypi.org/project/pgsqlx
