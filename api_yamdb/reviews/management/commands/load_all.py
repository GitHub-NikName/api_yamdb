import os
import csv
from django.core.management.base import BaseCommand

from reviews.models import User, Title, Genre, Review,\
    GenreTitle, Comment, Category


class Command(BaseCommand):
    help = 'load data from csv'

    FILES_DIR = 'static/data'
    data = [
        ['users.csv', User],
        ['genre.csv', Genre],
        ['category.csv', Category],
        ['review.csv', Review, 'author'],
        ['genre_title.csv', GenreTitle],
        ['comments.csv', Comment, 'author'],
        ['titles.csv', Title, 'category'],
    ]

    def load_csv(self, file, class_name, field=None):
        path = os.path.join(self.FILES_DIR, file)
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                if field:
                    row[f'{field}_id'] = row.pop(field)
                    try:
                        obj, _ = class_name.objects.update_or_create(**row)
                        print('.', end='')
                    except csv.Error as e:
                        f'Не удалось загрузить: {e}'
            print(f'{file} added')

    def handle(self, *args, **options):
        for attrs in self.data:
            self.load_csv(*attrs)
