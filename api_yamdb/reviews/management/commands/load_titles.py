import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Title


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):
        csv_file = 'static/data/titles.csv'

        if not os.path.isfile(csv_file):
            print('file not found!')
            return

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                user, _ = Title.objects.update_or_create(**row)
        print('Ок')
