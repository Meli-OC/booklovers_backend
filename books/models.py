from django.db import models


class Category(models.Model):
    """ Categories table """
    category_name = models.CharField(max_length=255, unique=True, null=False, blank=False)

    def __str__(self):
        return self.category_name


class Author(models.Model):
    """ Authors table """

    author_name = models.CharField(max_length=255, unique=True,  null=False, blank=False)

    def __str__(self):
        return self.author_name


class Book(models.Model):
    """ Books table """

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    published_date = models.CharField(max_length=50)
    image_url = models.URLField()

    categories = models.ManyToManyField(Category, related_name="books")
    authors = models.ManyToManyField(Author, related_name="books")

    def __str__(self):
        return self.title


class Keyword(models.Model):
    keyword = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.keyword



