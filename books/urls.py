from django.urls import path
from .views import BookCreateView, BookListView, BookDetailView, BookUpdateView, BookDeleteView, ReviewCreateView, BookReviewsList, ReviewUpdateView, ReviewDeleteView, BookFilterView

urlpatterns = [
    path('2.1/create-book/', BookCreateView.as_view(), name='create_book'),
    path('2.2/list-books/', BookListView.as_view(), name='list-books'),
    path('2.3/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('2.4/<int:id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('2.5/<int:id>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('3.1/<int:book>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('3.2/<int:book_id>/reviews/', BookReviewsList.as_view(), name='book-reviews-list'),
    path('3.3/review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('3.3/review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('4.1/filter/', BookFilterView.as_view(), name='book-filter'),
]