from django.urls import path
from .views import ListBookView

urlpatterns = [
    path('books-list', ListBookView.as_view())
]
