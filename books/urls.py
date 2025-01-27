from django.urls import path
from .views import BookCreateView, BookListView, BookDetailView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('create-book/', BookCreateView.as_view(), name='create_book'),
    path('list-books/', BookListView.as_view(), name='list-books'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:id>/delete/', BookDeleteView.as_view(), name='book-delete'),

]