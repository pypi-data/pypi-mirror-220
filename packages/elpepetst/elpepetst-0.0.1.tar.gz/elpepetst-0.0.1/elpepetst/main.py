"""Main module for the package. This is the entry point for the package."""

import requests


def test_pkg_function():
    """Makes a test api request to a placeholder api and prints result"""
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1", timeout=5)
    print(response.json())
