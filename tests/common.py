import os.path


def get_path(data_file_name):
    return os.path.join(os.path.dirname(__file__), "data", data_file_name)
