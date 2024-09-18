import pickle
import os


def pickle_in(file, obj):
    with open(file, "wb") as f:
        pickle.dump(obj, f)


def unpickle(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return pickle.load(f)
    else:
        with open(file, "wb") as f:
            pickle.dump(0, f)
            return 0
