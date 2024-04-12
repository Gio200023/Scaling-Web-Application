import time
from locust import HttpUser, task, between
import random

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/")

    @task(3)
    def view_items(self):
        rand = random.randint(1,10)
        for item_id in range(2):
            self.client.put("/objs/test"+str(rand))
            time.sleep(1)

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})