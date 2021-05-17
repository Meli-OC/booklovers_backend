from django.urls import path
from .views import ListBookView, DetailBookView, AuthorListView, AuthorDetailView

urlpatterns = [
    path('books-list', ListBookView.as_view()),
    path('<int:pk>', DetailBookView.as_view()),
    path('authors-list', AuthorListView.as_view()),
    path('author/<int:pk>', AuthorDetailView.as_view())
]
