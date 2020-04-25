import mysql.connector
from mysql.connector import errorcode


def execute_query(query, *kargs):
    config = {
        'user': 'DbMysql06',
        'password': 'bowie',
        # 'host': '127.0.0.1', in local
        'host': 'mysqlsrv1.cs.tau.ac.il', # in production
        'database': 'DbMysql06',
        # 'port': '3305',  in local
        'port': '3306', # in production
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(query, kargs)
        my_list = []
        for event in cursor:
            my_list.append(event)
        cnx.close()
        return my_list
