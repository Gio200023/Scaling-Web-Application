from locust import FastHttpUser, task, constant
import random


class QuickstartUser(FastHttpUser):
    host = "http://localhost:80"
    wait_time = constant(0)
    ids = []

    def get_id(self):
        if len(self.ids) == 0:
            return None
        return random.choice(self.ids)

    @task
    def get_all(self):
        self.client.get(url="/")

    @task
    def get_one(self):
        id = self.get_id()
        if id is None:
            return self.get_all()
        self.client.get(url='/objs/' + id)

    @task
    def get_one_compressed(self):
        id = self.get_id()
        if id is None:
            return self.get_all()
        self.client.get(url='/objs/' + id)

    @task
    def create_or_update(self):
        id = self.get_id()
        if id is None:
            return self.get_all()
        self.client.put(url='/objs/' + id, data={'content': "XXXXRVDFBGSZDBTDZCDFGNDXBDXSDBDDGF"})

    @task
    def delete_one(self):
        id = self.get_id()
        if id is None:
            return self.get_all()
        self.client.delete(url='/objs/' + id)
