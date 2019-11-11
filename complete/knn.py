# The kNN code implemented using NumPy

import numpy as np
import db_func
from os import path

def display_data(v):
    """Display a given vector using print"""
    try:
        assert(type(v) is np.ndarray)
        assert(len(v.shape) == 1)
        assert(v.size % db_func.config["data-width"] == 0)
    except:
        print("Invalid v for display_data")
        return None

    # If the value is greater than 0, print a block for it. Otherwise, leave a space.
    for i in range(v.size // db_func.config["data-width"]):
        for j in range(db_func.config["data-width"]):
            if v[i * db_func.config["data-width"] + j] > 0:
                print('█', end = "")
            else:
                print(" ", end = "")
        print()

    return True


def construct_data_set():
    """Get dataset. Return a list of tuple (actual_value, data(in numpy array format))"""
    
    id_list = db_func.read_db_list()
    try:
        assert(id_list is not None)
    except Exception as e:
        print("construct_data_set failed because read_db_list failed.")
        print(e)
        return []

    # Keep only the data with actual value
    id_list = [item for item in id_list if item[1] is not None]

    data_set = []
    for item in id_list:
        try:
            data_set.append((item[1], db_func.read_one_data(item[0])))
        except Exception as e:
            print("load data %d failed"%(item[0],))
            print(e)
    
    return data_set

def generate_M(data_set):
    """Generate the M matrix from data_set, in order to calculate the MSE."""

    try:
        data_set_pure = [item[1] for item in data_set]
        data_set_pure = np.array([item[1] for item in data_set])

        return data_set_pure

    except Exception as e:
        print("generate_M failed")
        print(e)
        return None


def calculate_mse(v, M):
    """Calculate the mse for a vector v and every rows of a matrix M"""
    
    try:
        assert(type(v) is np.ndarray)
        assert(type(M) is np.ndarray)
        assert(len(v.shape) == 1)
        assert(len(M.shape) == 2)
    except Exception as e:
        print("Invalid format for v or M")
        print(e)
        return None
    
    # Take advantage of Numpy's broadcast mechanism: https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html
    result = ((v-M) ** 2).mean(axis=1)

    return result


def predict(v, k=None, test=False):
    """Predict the digit given a vector v"""

    if k is None:
        k = db_func.config["default-k"]
    else:
        try:
            assert(type(k) is int)
            assert(k > 0)
        except Exception as e:
            print("Invalid argument k for predict")
            print(e)
            return None
    
    data_set = construct_data_set()

    # Randomly choose one if no data
    if len(data_set) == 0:
        most_indices = np.random.choice(np.arange(0, 10))
    else:
        mse = calculate_mse(v, generate_M(data_set))
        
        if mse is None:
            most_indices = np.random.choice(np.arange(0, 10))
        else:
            actual_value = np.array([item[0] for item in data_set])
            min_indices = mse.argsort()[:db_func.config["default-k"]]

            mapped_indices = actual_value[min_indices]
            counts = np.bincount(mapped_indices)
            most_indices = counts.argmax()

    # Provide also the counts for test
    if test and len(data_set)>0:
        return most_indices, counts[most_indices]
    else:
        return most_indices

