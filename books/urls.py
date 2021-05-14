from django.urls import path
from .views import ListBookView, DetailBookView

urlpatterns = [
    path('books-list', ListBookView.as_view()),
    path('<int:pk>', DetailBookView.as_view())
]
