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

    @staticmethod
    def categories_db(books):
        """ put books' categories data into the table """
        for book in books:
            categories = book["volumeInfo"].get("categories")
            if categories is not None:
                for cat in categories:
                    try:
                        Category.objects.bulk_create(
                            [
                                Category(category_name=cat)
                            ]
                        )
                    except IntegrityError:
                        return "No category name available"

    @staticmethod
    def authors_db(books):
        """ put authors' name into the table """
        for book in books:
            authors = book["volumeInfo"].get("authors")
            if authors is not None:
                for author in authors:
                    try:
                        Author.objects.bulk_create(
                            [
                                Author(author_name=author)
                            ]
                        )
                    except IntegrityError:
                        return "No author name available"

    @staticmethod
    def books_db(books):
        """ put all books' data in the table """
        for data in books:
            book_info = data["volumeInfo"]
            book_title = book_info.get("title")
            book_description = book_info.get("description")
            book_published = book_info.get("publishedDate")
            book_image = book_info.get("imageLinks").get("thumbnail")
            book = Book.objects.create(
                title=book_title,
                description=book_description,
                published_date=book_published,
                image_url=book_image,
            )

            categories = []
            for cat in book_info.get("categories"):
                category, created = Category.objects.get_or_create(
                    category_name=cat
                )
                categories.append(category)
                book.categories.add(*categories)

            authors = []
            for author_name in book_info.get["authors"]:
                author, created = Author.objects.get_or_create(
                    author_name=author_name
                )
                authors.append(author)
                book.authors.add(*authors)

    def clean_data(self, books):
        return [book for book in books if self.is_valid(book)]

    @staticmethod
    def is_valid(book):
        for el in book:
            categories = book["volumeInfo"].get("categories")
            authors = book["volumeInfo"].get("authors")
            description = book["volumeInfo"].get("description")
            image = book["volumeInfo"].get("imageLinks")
            if (categories and authors and description and image) is None:
                return False
            if (categories and authors and description and image) == "":
                return False
            if not (categories and authors and description and image):
                return False

        return True

    def handle(self, *args, **options):
        self.clean_db()
        books_list = self.fetch_books()
        clean_books = self.clean_data(books_list)
        self.categories_db(clean_books)
        self.authors_db(clean_books)
        self.books_db(clean_books)
        self.stdout.write(self.style.SUCCESS("Done"))
