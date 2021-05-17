from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class ListBookView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class DetailBookView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # def get_queryset(self):
    #     book_id = self.kwargs['pk']
    #     return Book.objects.get(pk=book_id)


class AuthorListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BookSerializer

    def get_queryset(self):
        # personalization of the query for getting author's name through many to many relations
        author = Author.objects.get(pk=self.kwargs['pk'])
        return Book.objects.filter(authors=author)
