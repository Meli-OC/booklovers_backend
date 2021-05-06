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
            }
            r = requests.get(const.URL, parameters)
            data = r.json()["items"]
            for book in data:
                books.append(book)
        return books

    def categories_db(self, books):
        """ put books' categories data into the table """
        for book in books:
            categories = book["volumeInfo"].get("categories")

            for cat in categories:
                try:
                    Category.objects.bulk_create(
                        [
                            Category(category_name=cat)
                        ]
                    )
                except IntegrityError:
                    return "No category name available"

    def clean_data(self, books):
        return [book for book in books if self.is_valid(book)]

    @staticmethod
    def is_valid(book):
        for el in book:
            categories = book["volumeInfo"].get("categories")
            if categories is None:
                return False
            if categories == "":
                return False
            if not categories:
                return False

        return True

    def handle(self, *args, **options):
        self.clean_db()
        books_list = self.fetch_books()
        clean_books = self.clean_data(books_list)
        self.categories_db(clean_books)
        self.stdout.write(self.style.SUCCESS("Done"))
