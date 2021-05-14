from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer


class ListBookView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class DetailBookView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
