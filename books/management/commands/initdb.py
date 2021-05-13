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
            default=10000,
            help="Categories' number to fetch"
        )
        parser.add_argument(
            '--authors',
            type=int,
            default=10000,
            help="Authors' number to fetch"
        )
        parser.add_argument(
            '--books',
            type=int,
            default=10000,
            help="Books number to fetch"
        )

    @classmethod
    def clean_db(cls):
        """ Clear all data from the database """
        Category.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()

    @classmethod
    def fetch_books(cls):
        """
            Method to fetch books data from google books api with specific parameters
        """
        categories = const.BOOK_CATEGORIES
        keywords = const.KEYWORDS
        page_size = 10
        books = []
        for word in keywords:
            for category in categories:
                for page in range(1):
                    parameters = {
                        "printType": "books",
                        "q": f"{word}",
                        "subject": f"{category}",
                        "startIndex": page * page_size,
                        "maxResults": page_size
                    }
                    r = requests.get(const.URL, parameters)
                    data = r.json()["items"]
                    for book in data:
                        books.append(book)
            return books

    @classmethod
    def categories_db(cls, books):
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

    @classmethod
    def authors_db(cls, books):
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

    @classmethod
    def books_db(cls, books):
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
            for author_name in book_info.get("authors"):
                author, created = Author.objects.get_or_create(
                    author_name=author_name
                )
                authors.append(author)
                book.authors.add(*authors)

    def clean_data(self, books):
        return [book for book in books if self.is_valid(book)]

    @classmethod
    def is_valid(cls, book):
        for el in book:
            categories = book["volumeInfo"].get("categories")
            authors = book["volumeInfo"].get("authors")
            description = book["volumeInfo"].get("description")
            image = book["volumeInfo"].get("imageLinks")
            published_date = book["volumeInfo"].get("publishedDate")
            if (categories and authors and description and image and published_date) is None:
                return False
            if (categories and authors and description and image and published_date) == "":
                return False
            if not (categories and authors and description and image and published_date):
                return False

        return True

    def handle(self, *args, **options):
        self.clean_db()
        books_list = self.fetch_books()
        print(len(books_list))
        clean_books = self.clean_data(books_list)
        print(len(clean_books))
        self.categories_db(clean_books)
        self.authors_db(clean_books)
        self.books_db(clean_books)
        self.stdout.write(self.style.SUCCESS("Done"))
