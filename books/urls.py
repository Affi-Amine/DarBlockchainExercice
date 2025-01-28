from django.urls import path
from .views import BookCreateView, BookListView, BookDetailView, BookUpdateView, BookDeleteView, ReviewCreateView, BookReviewsList, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('create-book/', BookCreateView.as_view(), name='create_book'),
    path('list-books/', BookListView.as_view(), name='list-books'),
    path('<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('<int:id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('<int:id>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('3.1/<int:book>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('3.2/<int:book_id>/reviews/', BookReviewsList.as_view(), name='book-reviews-list'),
    path('3.3/review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('3.3/review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]