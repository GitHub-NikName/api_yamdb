import csv
import os

from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = 'load people from csv'
    # data = {
    #     User: 'users',
    # } #  TODO доделать для всех файлов

    def handle(self, *args, **options):
        csv_file = 'static/data/users.csv'

        if not os.path.isfile(csv_file):
            print('file not found!')
            return

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            cnt = {'all': 0, 'new': 0}
            for row in reader:
                user, created = User.objects.update_or_create(**row)
                cnt['all'] += 1
                if created:
                    cnt['new'] += 1
        print('всего: {all}, добавлено в бд: {new}'.format(**cnt))