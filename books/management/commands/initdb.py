import os
import requests
from django.core.exceptions import ValidationError

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
        page_size = 40
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
                        continue

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
                        continue

    @classmethod
    def books_db(cls, books):
        """ put all books' data in the table """
        for data in books:
            try:
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

                books_cat = book_info.get("categories")
                books_authors = book_info.get("authors")
                if (books_cat and books_authors) is not None:
                    categories = []
                    for cat in books_cat:
                        category, created = Category.objects.get_or_create(
                            category_name=cat
                        )
                        categories.append(category)
                        book.categories.add(*categories)

                    authors = []
                    for author_name in books_authors:
                        author, created = Author.objects.get_or_create(
                            author_name=author_name
                        )
                        authors.append(author)
                        book.authors.add(*authors)
            except (IntegrityError, AttributeError):
                continue

    def handle(self, *args, **options):
        self.clean_db()
        books_list = self.fetch_books()
        print(len(books_list))
        self.categories_db(books_list)
        self.authors_db(books_list)
        self.books_db(books_list)
        self.stdout.write(self.style.SUCCESS("Done"))
