import time
import requests

class TestProgram:
    def __init__(self):
        self.status = "initialized"
    def run(self):
        self.status = "running"
        response = requests.get("https://vkr-api.vyachik-dev.ru/api/okved_sections/")
        if response.status_code != 200:
            self.status = "failed"
            print("Failed to fetch data from the API", response.status_code)
            return
        facts = response.json()
        print("Fetched facts:", facts)
        self.status = "completed"
        print("Test job completed successfully")