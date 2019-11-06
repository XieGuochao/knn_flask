import db_func
import csv
from os import path
if __name__ == "__main__":
    db_func.load_config(False)
    db_func.setup_table(reconstruct=True)
    
    conn, tunnel = db_func.create_db_conn()
    cursor = conn.cursor()
    cursor.execute("USE %s"%(db_func.config["db"]))
    with open(path.join("dataset", "original_data.csv")) as f:
        sp = csv.DictReader(f)
        for row in sp:
            print(db_func.config["default-table"], int(row['id']), int(row['actual value']), int(row['predict value']))
            cursor.execute("INSERT INTO %s VALUES (%d, %d, %d)"%(db_func.config["default-table"], int(row['id']), int(row['actual value']), int(row['predict value'])))
        conn.commit()
    conn.close()
    tunnel.close()

    print("Setup success")