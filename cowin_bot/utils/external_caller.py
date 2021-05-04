import os
import requests
import json


class APIInterface:
    @staticmethod
    def post(route, data=None):
        url = route
        # print(f"url = {url}, data = {data}")
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(
                f"Call to {route} failed with {response.status_code} and response {response.text}"
            )
        return response.text

    @staticmethod
    def get(route, params=None):
        url = route
        print(f"url = {url}, params = {params}")
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(
                f"Call to {route} failed with {response.status_code} and response {response.text}"
            )
        return response.text

    @staticmethod
    def put(route, data=None):
        url = route
        # print(f"url = {url}, data = {data}")
        response = requests.put(url, json=data)
        if response.status_code != 200:
            raise Exception(
                f"Call to {route} failed with {response.status_code} and response {response.text}"
            )
        return response.text
