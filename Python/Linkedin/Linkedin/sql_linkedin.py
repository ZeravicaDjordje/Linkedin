import sqlite3

def connect_cursor(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # delete
    # cursor.execute("""DROP TABLE connections;""")
    return connection, cursor

def create_table(cursor, *arg):
    arg = arg[0]
    if len(arg) != 5:
        print('You have to pass 5 elements in tuple')
        exit(0)
    sql_command = """
    CREATE TABLE %s ( 
    %s INTEGER PRIMARY KEY, 
    %s VARCHAR(50), 
    %s VARCHAR(30), 
    %s VARCHAR(20));""" % (arg[0], arg[1], arg[2], arg[3], arg[4])
    try:
        cursor.execute(sql_command)
    except Exception as e:
        print('You alredy made that tabel', e)
    return arg

def insert_data(cursor, tup, *arg):
    arg = arg[0]
    print(len(arg))
    if len(arg)  != 5:
        print('You have to pass 5 elements in tuple')
        exit(0)
    if len(tup) != 3:
        print('You have to pass 3 values in tuple as string')
        exit(0)
    format_str = """INSERT INTO %s ( %s, %s, %s, %s)
    VALUES (NULL, "{name_surname}", "{company}", "{position}");""" % (arg[0], arg[1], arg[2], arg[3], arg[4])
    sql_command = format_str.format(name_surname=tup[0], company=tup[1], position=tup[2])
    cursor.execute(sql_command)

def fetch_data(cursor, tabel_name):
    cursor.execute("SELECT * FROM %s" % tabel_name) 
    print("fetchall:")
    result = cursor.fetchall() 
    for r in result:
        yield r

def save_data(connection):
    # never forget this, if you want changes to be saved:
    connection.commit()
    connection.close()
