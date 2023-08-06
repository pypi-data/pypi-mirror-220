import pickle

def sample_data():
    data = list(range(50))
    pickled_data = pickle.dumps(data)
    return pickled_data, data