import pandas as pd
import os

def load_data(path):
    data = pd.read_csv(path)
    print("Data Loaded Successfully!")
    print(data.head())
    return data

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    file_path = os.path.join(project_root, "data", "students.csv")

    load_data(file_path)