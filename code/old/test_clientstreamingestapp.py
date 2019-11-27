from locust import HttpLocust, TaskSet, task

class Client1(TaskSet):
    @task
    def index(self):
        # test POST
        self.client.post("/upload", json={"user_id": "client1", "data": {"part_id": "56709", "ts_date": "20180315", "ts_time": "19:02:36", "room": "bathroom"}})

class Client2(TaskSet):
    @task
    def index(self):
        # test POST
        self.client.post("/upload", json={"user_id": "client2","data": {"Year": "1991", "Length": "105", "Title": "Predator 2", "Subject": "Action"}})




class MyLocust1(HttpLocust):
    task_set = Client1
    min_wait = 5000
    max_wait = 10000


class MyLocust2(HttpLocust):
    task_set = Client2
    min_wait = 5000
    max_wait = 10000

