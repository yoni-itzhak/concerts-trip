import mysql.connector
from mysql.connector import errorcode

serverName = 'mysqlsrv1.cs.tau.ac.il'
user = 'DbMysql06'
password = 'bowie'
dbName = 'DbMysql06'


def execute_query():
    config = {
        'user': 'DbMysql06',
        'password': 'bowie',
        'host': '127.0.0.1',
        'database': 'DbMysql06',
        'port': '3305',
        'raise_on_warnings': True,
        # 'use_pure': True
    }
    cnx = mysql.connector.connect(**config)

    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor(buffered=True)
        print("here")
        # cursor.execute("CREATE TABLE test (test_num int);")
        # query = "INSERT INTO test (test_num) VALUES (7)"
        # number = 5
        # param = (number)
        # cursor.execute(query, param)
        # cursor.execute(query)
        # cnx.commit()
        query = "SELECT test_num FROM test"
        cursor.execute(query)
        # Returns long integer rows affected, if any
        # rows_affected=cursor.execute("SELECT ... ")

        result = []
        row = {}

        for (test_num) in cursor:
            row = {'num': test_num[0]}
            print(test_num[0])
            result.append(row)
            print(row)
            print("")
            row = {}

        print(result)

        cnx.close()


def query1():
    query = "SELECT test_num FROM test WHERE test_num = %s OR test_num = %s"
    kargs = (12, 5)
    # param = (kargs,)
    execute_query(query, kargs)


# query1()
execute_query()
