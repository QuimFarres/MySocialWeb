from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
import concurrent.futures
import time

class CreatePostEfficiencyTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpassword')
        self.user2 = User.objects.create_user(username='user2', password='testpassword')
        self.client1 = self.client_class()
        self.client2 = self.client_class()
        self.client1.login(username='user1', password='testpassword')
        self.client2.login(username='user2', password='testpassword')

    def create_post(self, client, text):
        return client.post(reverse('create_post'), {'text': text})

    def test_create_100_posts_parallel_efficiency(self):
        start_time = time.time()

        post_text = 'Test post'

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(self.create_post, self.client1, post_text) for _ in range(50)]
            futures += [executor.submit(self.create_post, self.client2, post_text) for _ in range(50)]

            for future in concurrent.futures.as_completed(futures):
                response = future.result()
                self.assertEqual(response.status_code, 302)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Time taken to create 100 posts (parallel): {execution_time} seconds")
        

class CreatePostEfficiencyTestSingeUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_100_posts_efficiency(self):
        start_time = time.time()

        for _ in range(100):
            response = self.client.post(reverse('create_post'), {'text': 'Test post'})
            self.assertEqual(response.status_code, 302)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Time taken to create 100 posts: {execution_time} seconds")

