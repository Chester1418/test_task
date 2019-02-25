import json
import os
from faker import Faker
import requests
import random


class Bot(object):
    HEADERS = {
        "Content-Type": "application/json",
    }

    SIGNUP_URL = 'http://localhost:8000/api/signup/'
    LOGIN_URL = 'http://localhost:8000/api-token-auth/'
    POST_URL = 'http://localhost:8000/api/posts/'

    def __init__(self, json_data=None):
        if json_data:
            self.json = json_data
        else:
            raise BaseException("You didn't set json data or path to json.")

        self.number_of_users = self.json['number_of_users'] if self.json.get('number_of_users') else 1
        self.max_posts_per_user = self.json['max_posts_per_user'] if self.json.get('max_posts_per_user') else 1
        self.max_likes_per_user = self.json['max_likes_per_user'] if self.json.get('max_likes_per_user') else 1

        self.fake = Faker()

    def signup_users(self):
        self.users_list = []
        users_number = self.number_of_users
        while users_number:
            request_data = {
                "username": self.fake.user_name(),
                "password": self.fake.password(),
                "email": self.fake.email()
            }
            response = requests.post(url=self.SIGNUP_URL, data=json.dumps(request_data), headers=self.HEADERS)

            if not response.status_code == 201:
                raise BaseException(response.content)
            self.users_list.append(request_data)
            users_number -= 1
        print(f'Generated {self.number_of_users} users')

    def login_users(self):
        self.jwt_tokens = []
        for user in self.users_list:
            response = requests.post(url=self.LOGIN_URL, data=json.dumps(user), headers=self.HEADERS)
            if response.status_code == 200:
                self.jwt_tokens.append(json.loads(response.content))

    def create_posts(self):
        self.post_ids = []
        for user_token in self.jwt_tokens:
            user_max_posts = random.randint(0, self.max_posts_per_user)
            self.HEADERS['Authorization'] = f'JWT {user_token["token"]}'
            while user_max_posts:
                request_data = {
                    "title": self.fake.paragraph()[:200],
                    "text": self.fake.text()
                }

                response = requests.post(url=self.POST_URL, data=json.dumps(request_data), headers=self.HEADERS)

                if not response.status_code == 201:
                    raise BaseException(response.content)

                self.post_ids.append(json.loads(response.content)['id'])
                user_max_posts -= 1
        print("All posts were created")

    def _like_post(self, post_id, user):
        self.HEADERS['Authorization'] = f'JWT {user["token"]}'
        response = requests.get(url=self.POST_URL + f'{post_id}/like/', headers=self.HEADERS)

    def like_time(self):
        for user in self.jwt_tokens:
            max_like_per_user = self.max_likes_per_user
            while max_like_per_user:
                self._like_post(random.choices(self.post_ids)[0], user)
                max_like_per_user -= 1
        print('Users like some posts and reached their maximum')
