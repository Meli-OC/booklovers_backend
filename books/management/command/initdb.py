import os
import requests
import books.constants as const
from django.db import IntegrityError
from books.models import Author, Category, Book
from django.core.management.base import BaseCommand
from django.db.utils import DataError


class Command(BaseCommand):
    """ Class to handle database and fetch data and clean it """

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=2,
            help="Categories' number to fetch"
        )
        parser.add_argument(
            '--authors',
            type=int,
            default=2,
            help="Authors' number to fetch"
        )
        parser.add_argument(
            '--books',
            type=int,
            default=2,
            help="Books number to fetch"
        )

    @staticmethod
    def clean_db():
        """ Clear all data from the database """
        Category.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()

    @staticmethod
    def fetch_books():
        """
            Method to fetch books data from google books api with specific parameters
        """
        categories = const.BOOK_CATEGORIES
        books = []
        for category in categories:
            parameters = {
                "q": f"incategory:{category}",
                "key": os.getenv("GOOGLE_API_KEY")
            }
            r = requests.get(const.URL, parameters)
            data = r.json()["items"]
            for book in data:
                book["volumeInfo"][categories] = f"{category}, {book['categories']}"
                books.append(book)
