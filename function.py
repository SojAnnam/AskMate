import csv
import base64
import time
import datetime
import psycopg2


def sql_query_get(query):
    try:
        connect_str = "dbname='markorkenyi' user='markorkenyi' host='localhost' password='shadow123'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
    cur.execute(query)
    table = cur.fetchall()
    table = (list(map(list, table)))
    return table


def sql_query_post(query):
    try:
        connect_str = "dbname='markorkenyi' user='markorkenyi' host='localhost' password='shadow123'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
    cur.execute(query)
    conn.close()
    return None


def convert_time(input_, type_):
    '''Converts time from UNIX to readable format, or vice-versa'''
    if type_ == "encode":
        datetime_obj = datetime.datetime.strptime(str(input_), ("%Y-%m-%d %H:%M:%S"))
        tuple_ = datetime_obj.timetuple()
        return time.mktime(tuple_)
    elif type_ == "decode":
        return input_.strftime("%Y-%m-%d %H:%M:%S")


def get_new_id(filepath, type_of_csv):
    '''Returns a new ID for the entry. If no entry is present, the first ID will be 1'''
    id_ = ['0']
    data = read_csv(filepath, type_of_csv)
    for row in data:
        id_.append(row[0])
    max_id = max(map(int, id_))
    return (int(max_id) + 1)


def remove(file_data, id_, index_):
    '''Removes the matching row from the csv_data, and returns csv_data'''
    to_pop = []
    for index, elements in enumerate(file_data):
        if elements[index_] == id_:
            to_pop.append(index)
    for i in reversed(list(map(int, to_pop))):
        file_data.pop(i)
    return file_data
