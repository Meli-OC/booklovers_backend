from rest_framework import serializers
from .models import Book, Category, Author


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('id', 'title', 'description', 'published_date', 'authors')