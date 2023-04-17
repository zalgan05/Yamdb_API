import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=False,
            help='Удалить записи',
        )

    def handle(self, *args, **options):
        Models = [
            Category,
            Genre,
            Title,
            User,
            Review,
            Comment,
        ]
        for model in Models:
            if options["delete_existing"]:
                model.objects.all().delete()

        for model in Models:
            objects = []
            with open(
                f"static/data/{model.__name__.lower()}.csv",
                'r',
                encoding='utf-8',
            ) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    objects.append(model(**row))
                model.objects.bulk_create(objects)

        with open("static/data/genre_title.csv", 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title_genre = [(row["title_id"], row["genre_id"])]
                for title_id, genre_id in title_genre:
                    title = Title.objects.get(id=title_id)
                    genre = Genre.objects.get(id=genre_id)
                    title.genre.add(genre)
