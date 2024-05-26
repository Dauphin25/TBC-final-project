# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (register, CustomLoginView, dashboard, reserve_book, reservation_success, user_reserved_books,
                    issue_book, issue_success, active_issued_books, mark_as_returned, returned_books_history, add_book,
                    update_book, delete_book, book_list, reserved_books_list)

urlpatterns = [
    path('add-book/', add_book, name='add_book'),
    path('update-book/<int:pk>/', update_book, name='update_book'),
    path('delete-book/<int:pk>/', delete_book, name='delete_book'),
    path('books/', book_list, name='book_list1'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('reserve-book/', reserve_book, name='reserve_book'),
    path('reservation-success/', reservation_success, name='reservation_success'),
    path('my-reserved-books/', user_reserved_books, name='user_reserved_books'),
    path('issue-book/', issue_book, name='issue_book'),
    path('issue-success/', issue_success, name='issue_success'),
    path('active-issued-books/', active_issued_books, name='active_issued_books'),
    path('mark-as-returned/<int:pk>/', mark_as_returned, name='mark_as_returned'),
    path('returned-books-history/', returned_books_history, name='returned_books_history'),
    path('reserved-books/', reserved_books_list, name='reserved_books_list'),

]
