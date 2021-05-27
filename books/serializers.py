from rest_framework import serializers
from .models import Book, Category, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'author_name', 'books')


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'published_date', 'authors', 'image_url')
        read_only_fields = ('id', 'title', 'description', 'published_date', 'authors', 'image_url')
