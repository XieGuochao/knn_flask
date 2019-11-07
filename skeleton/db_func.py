import pymysql
import numpy as np
import json
import sys
from sshtunnel import SSHTunnelForwarder
from os import path

config = None

def load_config(test = False, config_file = "config.json"):
    """Load the configuration from config.json, exit if fail"""

    global config
    with open(config_file, "r") as f:
        config = json.load(f)
    print("config:", config)

    for key in config:
        # Check if every configuration is set
        if config[key]=="":
            print("Please complete the config.json first!")
            sys.exit(1)
    else:
        config["default-k"] = int(config["default-k"])
        if test:
            config["default-suffix"] = config["test-suffix"]
            config["default-table"] = "knn_"+config['test-suffix']
            config["data-width"] = 3
        else:
            config["default-suffix"] = config["suffix"]
            config["default-table"] = "knn_" + config["suffix"]
            config["data-width"] = int(config["data-width"])

        print("Configuration Check success")


def read_db_list(tablename = None):
    """Read all data from db. Return a list of tuple (id, actual_value, predict_value)."""

    # Set the default tablename
    if tablename is None:
        tablename = config["default-table"]

    conn, tunnel = create_db_conn()
    result = None

    try:
        cur = conn.cursor()
        
        # Task: need to execute 2 SQL queries: 
        # 1. Use the database in config
        # 2. Select everything from the tablename



        conn.commit()
        result = cur.fetchall()

    except Exception as e:
        print("read_data_list failed")
        print(e)

    conn.close()
    tunnel.close()
    return result


def read_db_one(id, tablename = None):
    """Read a record from db. Return a tuple (id, actual_value, predict_value)."""

    # Set the default tablename
    if tablename is None:
        tablename = config["default-table"]

    conn, tunnel = create_db_conn()
    result = None

    try:
        cur = conn.cursor()

        # Task: need to execute 2 SQL queries:
        # 1. Use the database in config
        # 2. Select everything with the specific id from the table tablename



        conn.commit()
        result = cur.fetchone()
        if len(result) == 0:
            result = None

    except Exception as e:
        print("read_data_list failed")
        print(e)

    conn.close()
    tunnel.close()
    return result


def read_one_data(data_id):
    """Read a specific from dataset. Return a numpy object."""
    
    read_data = None

    try:
        # Task: load the data from data directory with the specific data_id
        # You may need to use the following 2 functions:
        # 1. np.load
        # 2. path.join



        pass

    except Exception as e:
        print("read_one_data failed: {}", data_id)
        print(e)

    return read_data


def insert_data(v):
    """Save a vector and insert a record in the database."""
    
    try:
        assert(type(v) is np.ndarray)
    except:
        print("The input v should be a numpy array!")
        return None
    
    conn, tunnel = create_db_conn()
    cur = conn.cursor()

    last_id = None
    
    # Reference: https://dev.mysql.com/doc/connector-odbc/en/connector-odbc-usagenotes-functionality-last-insert-id.html
    
    try:
        # Task: need to execute 3 SQL queries:
        # 1. use the database in config
        # 2. insert a null record into the default table
        # 3. select the last id we have inserted; you may go to the reference link for more information



        conn.commit()
        last_id = cur.fetchone()[0]
        print("last_id:", last_id)

        # Task: save the vector v into a file in data directory with the name using the last id we have inserted
        # You may need to use the following 2 functions:
        # 1. np.save
        # 2. path.join




    except Exception as e:
        print("insert_data failed")
        print(e)

    conn.close()
    tunnel.close()
    return last_id

    
def update_actual_value(data_id, actual_value):
    """Update the actual value of data_id in the database."""
    conn, tunnel = create_db_conn()
    cur = conn.cursor()
    
    result = None

    try:
        # Task: you need to execute the following 2 SQL queries:
        # 1. use the database in config
        # 2. update the actual value in the table with the specific data_id



        conn.commit()
        print("update_actual_value succeeded")
        result = True

    except Exception as e:
        print("update_actual_value failed")
        print(e)

    conn.close()
    tunnel.close()

    return result


def update_predict_value(data_id, predict_value):
    """Update the predict value of data_id in the database."""
    conn, tunnel = create_db_conn()
    cur = conn.cursor()
    
    result = None

    try:
        # Task: you need to execute the following 2 SQL queries:
        # 1. use the database in config
        # 2. update the predict value in the table with the specific data_id



        conn.commit()
        print("update_predict_value succeeded")
        result = True

    except Exception as e:
        print("update_predict_value failed")
        print(e)

    conn.close()
    tunnel.close()

    return result


def create_ssh_tunnel():
    """Create an SSH tunnel to access the database"""
    
    # Reference link: https://sshtunnel.readthedocs.io/en/latest/
    tunnel = SSHTunnelForwarder(
        (config['ip'], 22),
        ssh_username=config['username'],
        ssh_password=config["ssh-password"],
        remote_bind_address=('localhost', 3306),
    )

    tunnel.start() 
    print("SSH Connected") 
    return tunnel


def create_db_conn():
    """Create and return a SSH Tunnel for MySQL connection. Require manual close after usage."""
    
    # Using SSH Tunnel because professor has closed the 3306 port from external access.
    tunnel = create_ssh_tunnel()
    conn = pymysql.Connect(host='127.0.0.1',
                            port=tunnel.local_bind_port,
                            user=config['username'],
                            passwd=config['db-password'])
    return conn, tunnel

def check_table(table_name = None):
    """Check if the table exist."""

    if table_name is None:
        table_name = config["default-table"]

    conn, tunnel = create_db_conn()
    
    result = None

    try:
        cur = conn.cursor()

        # Task: check the existing of a table.
        # One possible way:
        # 1. use the table in config
        # 2. show tables
        # 3. fetch all the results and see if the table_name is in the results
        # You may come up with other solutions!
        # You should save your result (True / False) into "result"
        

        
    except Exception as e:
        print("check_table FAILED")
        print(e)

    conn.close()
    tunnel.close()
    return result


def setup_table(table_name = None, reconstruct = False):
    """Create the template table for this project."""
    
    if table_name is None:
        table_name = config["default-table"]

    conn, tunnel = create_db_conn()
    try:
        cur = conn.cursor()

        # Task: you should first use the database in the config



        # Task: if reconstruct is True, you should drop the table and create a table with the following attributes:
        # 1. id INT UNSIGNED AUTO_INCREMENT (Question: what is the usage of auto_increment?)
        # 2. `actual value` INT UNSIGNED
        # 3. `predict value` INT UNSIGNED
        # 4. PRIMARY KEY(`id`)



        # The following shows a way to test if the table has been created successfully.
        cur.execute("""
            SHOW TABLES;
            """)
        conn.commit()
        
        all_tables = cur.fetchall()
        assert((table_name,) in all_tables)
        print("setup_table PASSED")
    except Exception as e:
        print("setup_table FAILED")
        print(e)

    conn.close()
    tunnel.close()

        