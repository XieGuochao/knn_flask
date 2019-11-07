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
    
    # Task: filter out the data without actual value, because they cannot be used in the model; save the remaining id in a list



    data_set = []

    # Task: try to load the data's actual value and the numpy array data, and save the result as a tuple in data_set
    # You may use "read_one_data" function defined in db_func



    return data_set

def generate_M(data_set):
    """Generate the M matrix from data_set, in order to calculate the MSE."""

    try:
        data_set_pure = None

        # Task: from the data_set, you should join all numpy row vectors into a matrix data_set_pure (pure means we do not save the actual value here)



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
    
    result = None

    # Task: calculate the mean squared error for each row in M versus vector v. Hint: you may take advantage of Numpy's broadcast mechanism.
    # Take advantage of Numpy's broadcast mechanism: https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html
    
    



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
        most_indices = None
        
        # Task: aggregate the functions you have implemented and come up with the most indices, save it as most_indices.
        # You may follow the 6 stesp:
        # 1. calculate the mean squared error vector
        # 2. collect the actual_value vector from the data_set
        # 3. get the indices with the minimal k mean squared errors
        # 4. get the actual values with the smallest k MSE from your actual_value vector
        # 5. count the number of indices
        # 6. find the most indices from the count




    # Provide also the counts for test
    if test and len(data_set)>0:
        return most_indices, counts[most_indices]
    else:
        return most_indices

