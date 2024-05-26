from library.views.home import home
from django.urls import path
from library.views.book import BookListView, BookDetailView
from library.views.author import AuthorListView, AuthorDetailView

urlpatterns = [
    path('', home, name='home'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),

]
