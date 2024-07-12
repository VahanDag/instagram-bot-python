import csv
import json


def load_credentials(file_path="credentials.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def load_comments(file_path="comments.csv"):
    with open(file_path, "r") as f:
        return [row[0] for row in csv.reader(f)]
