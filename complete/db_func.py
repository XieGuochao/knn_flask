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
            config["data-dir"] += "_test"
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
        cur.execute("USE %s"%(config['db']))
        cur.execute("SELECT * FROM %s;"%(tablename,))
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
        cur.execute("USE %s"%(config['db']))
        cur.execute("SELECT * FROM %s WHERE id = %d;"%(tablename,id))
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
        read_data = np.load(path.join(config["data-dir"], "{}.npy".format(data_id)))
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
        cur.execute("USE %s;"%(config['db']))
        cur.execute("INSERT INTO %s () VALUES ();"%(config["default-table"]))
        cur.execute("SELECT LAST_INSERT_ID();")

        conn.commit()
        last_id = cur.fetchone()[0]
        print("last_id:", last_id)

        np.save(path.join(config["data-dir"], str(last_id)), v)

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
        cur.execute("USE %s"%(config['db']))
        cur.execute("UPDATE `%s` SET `actual value` = %d WHERE id = %d;"%(config["default-table"], actual_value, data_id))
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
        cur.execute("USE %s"%(config['db']))        
        cur.execute("UPDATE `%s` SET `predict value` = %d WHERE id = %d;"%(config["default-table"], predict_value, data_id))
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
        cur.execute("""
            USE %s
            """%(config['db'], ))

        cur.execute("""
            SHOW TABLES;
            """)
        
        all_tables = cur.fetchall()
        if (table_name,) in all_tables:
            result = True
        else:
            result = False
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
        cur.execute("""
            USE %s
            """%(config['db'], ))

        if reconstruct:
            cur.execute("""
                DROP TABLE IF EXISTS `%s`;
                """%(table_name,))
            cur.execute("""CREATE TABLE `%s` (
                    `id` INT UNSIGNED AUTO_INCREMENT,
                    `actual value` INT UNSIGNED,
                    `predict value` INT UNSIGNED,
                    PRIMARY KEY(`id`)
                )
                ;"""%(table_name,))
            conn.commit()

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

        