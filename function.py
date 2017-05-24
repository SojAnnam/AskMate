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


def vote_update_sql_query(table, _id, direction):
    select_query = ("SELECT vote_number FROM {} WHERE id={};".format(table, _id))
    vote_number = sql_query_get(select_query)
    votes = int(vote_number[0][0])
    if direction == 'up':
        votes += 1
    elif direction == 'down':
        votes -= 1
    sql_to_edit_vote = ("UPDATE {} SET vote_number= {} WHERE id= {};".format(
        table, votes, _id))
    sql_query_post(str(sql_to_edit_vote))
