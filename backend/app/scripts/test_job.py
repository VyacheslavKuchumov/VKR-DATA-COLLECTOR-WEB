import time

class TestProgram:
    def __init__(self):
        self.status = "initialized"
    def run(self):
        self.status = "running"
        for i in range(100):
            print(f"Test job is running: {i}")
            time.sleep(1)
        self.status = "completed"
        print("Test job completed successfully")