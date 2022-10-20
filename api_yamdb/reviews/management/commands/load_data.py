from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

files_to_download = {User: 'static/data/users.csv',
                     Category: 'static/data/category.csv',
                     Genre: 'static/data/genre.csv',
                     Title: 'static/data/titles.csv',
                     Review: 'static/data/review.csv',
                     Comment: 'static/data/comments.csv',
                     'Genre_Title': 'static/data/genre_title.csv',
                     }


class Command(BaseCommand):
    """Класс реализует загрузку данных из csv в таблицы моделей проекта."""
    help = 'Загрузка данных из .csv в модели проекта.'

    def handle(self, *args, **options):
        for model, file in files_to_download.items():
            print(f'Загрузка данных из файла {file} в модель {model}...')

            for row in DictReader(open(f'./{file}')):
                if model == User:
                    obj = model(id=row['id'], username=row['username'],
                                email=row['email'], role=row['role'],
                                bio=row['bio'], first_name=row['first_name'],
                                last_name=row['last_name'])
                    obj.save()
                elif model == Category or model == Genre:
                    obj = model(id=row['id'], name=row['name'],
                                slug=row['slug'])
                    obj.save()
                elif model == Title:
                    obj = model(id=row['id'], name=row['name'],
                                year=row['year'], category_id=row['category'])
                    obj.save()
                elif model == Review:
                    obj = model(id=row['id'], title_id=row['title_id'],
                                text=row['text'], author_id=row['author'],
                                score=row['score'], pub_date=row['pub_date'])
                    obj.save()
                elif model == Comment:
                    obj = model(id=row['id'], review_id=row['review_id'],
                                text=row['text'], author_id=row['author'],
                                pub_date=row['pub_date'])
                    obj.save()
                else:
                    genre = Genre.objects.get(pk=row['genre_id'])
                    title = Title.objects.get(pk=row['title_id'])
                    title.genre.add(genre)
        print(f'Загрузка данных завершена!')
