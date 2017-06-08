import psycopg2


def get_config():
    """ Import credential for database access"""
    with open("config.txt") as config:
        config = config.readlines()
    return config


def db_request(query):
    """Establish connection for database request"""
    config = get_config()
    try:
        connect_str = "dbname={} user={} host='localhost' password={}".format(config[0], config[0], config[1])
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
    cur.execute(query)
    table = cur.fetchall()
    table = (list(map(list, table)))
    return table


def db_update(query):
    """Establish connection for database update"""
    config = get_config()
    try:
        connect_str = "dbname={} user={} host='localhost' password={}".format(config[0], config[0], config[1])
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
    cur.execute(query)
    conn.close()
    return None
