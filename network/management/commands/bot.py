from django.core.management.base import BaseCommand
from rest_framework.utils import json

from network_bot.bot import Bot


class Command(BaseCommand):
    help = "Automated bot to emulate create signup users, create posts, randomly like them"

    def add_arguments(self, parser):
        parser.add_argument('--data', nargs='?', type=str)

    def handle(self, *args, **options):
        data = json.load(open(options.get("data"), 'r'))

        bot = Bot(data)
        bot.signup_users()
        bot.login_users()
        bot.create_posts()
        bot.like_time()
