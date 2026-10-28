from faker import Faker
from locust import HttpUser, task, SequentialTaskSet, TaskSet, constant_throughput
import random

fake = Faker('ru_RU')

class Shopping(SequentialTaskSet):
    
    @task
    def view_products(self):
        self.client.get('/api/products', name='/api/products [GET]')

    @task
    def add_to_cart(self):
        item = {
            'product_id': random.randint(1, 100),
            'name': fake.word(),
            'quantity': random.randint(1, 5)
        }
        self.client.post('/api/cart', data=item, name='/api/cart [POST]')
        self.interrupt()

class Browsing(TaskSet):

    @task(5)
    def view_products(self):
        self.client.get('/api/products', name='/api/products [GET]')

    @task(5)
    def view_cart(self):
        self.client.get('/api/cart', name='/api/cart [GET]')

    @task(5)
    def view_profile(self):
        self.client.get('/api/profile', name='/api/profile [GET]')

    @task(5)
    def check_metrics(self):
        self.client.get('/metrics', name='/metrics [GET]')

    @task(5)
    def check_home(self):
        self.client.get('/', name='/ [GET]')

    @task(1)
    def quick_add_to_cart(self):
        item = {'product_id': random.randint(1, 100), 'quantity': 1}
        self.client.post('/api/cart', data=item, name='/api/cart [POST]')

class WebsiteUser(HttpUser):
    host = "http://localhost:8080"
    wait_time = constant_throughput(2)
    tasks = [Shopping, Browsing]