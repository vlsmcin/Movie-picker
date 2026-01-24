import requests
from movies.models import Genre
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fill genres from TMDB API'

    def handle(self, *args, **kwargs):
        if (Genre.objects.all().count() > 0):
            self.stdout.write(self.style.WARNING("Genres already filled."))
            return

        url = "https://api.themoviedb.org/3/genre/movie/list?language=pt"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            for genre in data['genres']:
                g = Genre(tmdb_id=genre['id'], name=genre['name'])
                g.save()

            self.stdout.write(self.style.SUCCESS("Genres filled successfully."))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"An error occurred while filling genres: {str(e)}"))