from flask import Flask, Response, request
from os import path
import db_func, knn
import numpy as np
app = Flask(__name__, static_url_path = "/static", static_folder = "static")

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json['data']
    print(data)
    new_index = db_func.insert_data(np.array(data))
    
    return Response(str(new_index))

@app.route('/api/result/<int:id>')
def result(id):
    print("id:", id)
    predict_value = knn.predict(db_func.read_one_data(id))
    db_func.update_predict_value(id, predict_value)

    return Response(str(predict_value))


@app.route('/api/update_actual_value', methods=['POST'])
def update_actual_value():
    id = int(request.json['id'])
    actual_value = int(request.json['actual_value'])
    print(id, actual_value)
    assert(db_func.update_actual_value(id, actual_value))

    return "OK"


if __name__ == '__main__':
    db_func.load_config(False)

    if not db_func.check_table():
        db_func.setup_table(reconstruct = True)

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(threaded = True, debug = True)