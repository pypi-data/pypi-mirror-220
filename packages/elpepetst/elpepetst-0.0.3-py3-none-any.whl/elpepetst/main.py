"""Main module for the package. This is the entry point for the package."""
import json
import os

import requests


def test_pkg_function():
    """Makes a test api request to a placeholder api and prints result"""
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1", timeout=5)
    print(response.json())


def test_json_function():
    """Makes a test api request to a placeholder api and prints result"""
    # read json file
    file_path = os.path.join(os.path.dirname(__file__), "assets/static.json")

    with open(file_path, encoding="utf-8") as json_file:
        data = json.load(json_file)
        print(data)


if __name__ == "__main__":
    test_json_function()