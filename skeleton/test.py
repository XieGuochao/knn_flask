import db_func, knn
import numpy as np


if __name__ == "__main__":
    db_func.load_config(True)

    # Test Initialization of Table
    db_func.setup_table("knn_" + db_func.config["test-suffix"], True)

    test_data = np.array([1, 1, 0, 
                          0, 1, 0, 
                          1, 1, 1])

    new_id = db_func.insert_data(test_data)

    assert(db_func.read_db_list() is not None)
    assert(new_id == 1)
    print("read_db_list test PASS")

    read_data = db_func.read_one_data(new_id)
    assert(np.array_equal(test_data, read_data))
    print("read_data & insert_data test PASS")

    predict_value = 2
    actual_value = 1
    assert(db_func.update_predict_value(new_id, predict_value))
    assert(db_func.update_actual_value(new_id, actual_value))

    query_data = db_func.read_db_one(new_id)
    assert(query_data == (new_id, actual_value, predict_value))
    print("update_predict_value, update_actual_value, read_db_one test PASS")


    assert(knn.display_data(db_func.read_one_data(new_id)))
    print("display_data test PASS")

    assert(len(knn.construct_data_set()) > 0)
    print("construct_data_set test PASS")

    test_data_2 = np.array([1, 1, 1, 
                          0, 1, 0, 
                          1, 1, 1])

    actual_value_2 = 2
    new_id_2 = db_func.insert_data(test_data_2)
    assert(new_id_2 == 2)
    assert(db_func.update_actual_value(new_id_2, actual_value_2))

    data_set = knn.construct_data_set()
    assert(len(data_set) == 2)
    v = np.array([0, 0, 0, 
                  0, 0, 0, 
                  0, 0, 0])
    M = knn.generate_M(data_set)
    assert(np.array_equal(M, np.array([[1, 1, 0, 0, 1, 0, 1, 1, 1],
                                       [1, 1, 1, 0, 1, 0, 1, 1, 1]])))
    
    real_mse = np.array([2/3, 7/9])
    assert(np.array_equal(knn.calculate_mse(v, M), real_mse))

    print("generate_M and calculate_mse test PASS")

    # Insert again test_data and test_data_2 to check robustness of predict
    new_id_3 = db_func.insert_data(test_data)
    db_func.update_actual_value(new_id_3, actual_value)

    new_id_4 = db_func.insert_data(test_data_2)
    db_func.update_actual_value(new_id_4, actual_value_2)

    predict_1 = knn.predict(test_data, test=True)
    assert(predict_1 == (1, 2))
    predict_2 = knn.predict(test_data_2, test=True)
    assert(predict_2 == (2, 2))

    print("predict test PASS")