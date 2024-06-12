# views.py
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView

from django.utils import timezone


from users.forms import BookForm, UpdateIsTakenForm
from library.models.book import Book

from library.models import IssuedBook
from .forms import LibraryUserRegistrationForm, LibraryUserLoginForm, ReserveBookForm, IssueBookForm


from django.views.generic import ListView
from library.models import ReserveBook
from django.contrib.auth.mixins import UserPassesTestMixin
from library.models import IssuedBook
from django.db import models


def register(request):
    if request.method == 'POST':
        form = LibraryUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = LibraryUserRegistrationForm()
    return render(request, 'users/registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = LibraryUserLoginForm
    template_name = 'users/login.html'


@login_required
def user_reserved_books(request):
    search_query = request.GET.get('q', '')
    sort_order = request.GET.get('sort', 'newest')
    user_info = request.user

    active_reserved_books = ReserveBook.objects.filter(user=request.user.library_user, is_taken=False, status='active')
    canceled_reserved_books = ReserveBook.objects.filter(user=request.user.library_user, status='canceled')
    history_reserved_books = ReserveBook.objects.filter(user=request.user.library_user, is_taken=True)

    if search_query:
        active_reserved_books = active_reserved_books.filter(book__title__icontains=search_query)
        canceled_reserved_books = canceled_reserved_books.filter(book__title__icontains=search_query)
        history_reserved_books = history_reserved_books.filter(book__title__icontains=search_query)

    if sort_order == 'newest':
        active_reserved_books = active_reserved_books.order_by('-reserved_date')
        canceled_reserved_books = canceled_reserved_books.order_by('-reserved_date')
        history_reserved_books = history_reserved_books.order_by('-reserved_date')
    elif sort_order == 'oldest':
        active_reserved_books = active_reserved_books.order_by('reserved_date')
        canceled_reserved_books = canceled_reserved_books.order_by('reserved_date')
        history_reserved_books = history_reserved_books.order_by('reserved_date')

    return render(request, 'users/user_reserved_books.html', {
        'active_reserved_books': active_reserved_books,
        'canceled_reserved_books': canceled_reserved_books,
        'history_reserved_books': history_reserved_books,
        'search_query': search_query,
        'sort_order': sort_order,
        'user_info': user_info,
    })


def is_librarian(user):
    return hasattr(user, 'librarian')


@user_passes_test(is_librarian)
def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            issued_book = form.save(commit=False)
            issued_book.issued_date = date.today()
            issued_book.save()
            issued_book.book.borrow_book()
            return redirect('active_issued_books')
    else:
        form = IssueBookForm()
    return render(request, 'users/issue_book.html', {'form': form})


@user_passes_test(is_librarian)
def issue_success(request):
    return render(request, 'users/issue_success.html')


@user_passes_test(is_librarian)
def active_issued_books(request):
    query = request.GET.get('q')
    issued_books = IssuedBook.objects.filter(returned=False)

    if query:
        issued_books = issued_books.filter(user__personal_identification_number__icontains=query)

    return render(request, 'users/active_issued_books.html', {
        'issued_books': issued_books,
        'query': query,
    })


@user_passes_test(is_librarian)
def mark_as_returned(request, pk):
    issued_book = get_object_or_404(IssuedBook, pk=pk)
    issued_book.returned = True
    issued_book.return_date = timezone.now().date()
    issued_book.save()
    return redirect('active_issued_books')


@user_passes_test(is_librarian)
def returned_books_history(request):
    query = request.GET.get('q')
    returned_books = IssuedBook.objects.filter(returned=True)

    if query:
        returned_books = returned_books.filter(user__personal_identification_number__icontains=query)

    return render(request, 'users/returned_books_history.html', {
        'returned_books': returned_books,
        'query': query,
    })


@user_passes_test(is_librarian)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'users/book_form.html', {'form': form, 'title': 'Add Book'})


@user_passes_test(is_librarian)
def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'users/book_form.html', {'form': form, 'title': 'Update Book'})


@user_passes_test(is_librarian)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'users/confirm_delete.html', {'book': book})


@user_passes_test(is_librarian)
def book_list(request):
    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(Q(title__icontains=query))
    else:
        books = Book.objects.all()

    return render(request, 'users/book_list1.html', {'books': books, 'query': query})


@user_passes_test(is_librarian)
def reserved_books_list(request):
    query = request.GET.get('q')

    if request.method == 'POST':
        form = UpdateIsTakenForm(request.POST)
        if form.is_valid():
            reservation_id = request.POST.get('reservation_id')
            reservation = get_object_or_404(ReserveBook, id=reservation_id)
            reservation.is_taken = form.cleaned_data['is_taken']
            reservation.save()
            return redirect('reserved_books_list')

    active_reserved_books = ReserveBook.objects.filter(status='active', is_taken=False)
    canceled_reserved_books = ReserveBook.objects.filter(status='canceled')
    taken_reserved_books = ReserveBook.objects.filter(status='active', is_taken=True)

    if query:
        active_reserved_books = active_reserved_books.filter(
            Q(user__personal_identification_number__icontains=query)
        )
        canceled_reserved_books = canceled_reserved_books.filter(
            Q(user__personal_identification_number__icontains=query)
        )
        taken_reserved_books = taken_reserved_books.filter(
            Q(user__personal_identification_number__icontains=query)
        )

    form = UpdateIsTakenForm()

    context = {
        'active_reserved_books': active_reserved_books,
        'canceled_reserved_books': canceled_reserved_books,
        'taken_reserved_books': taken_reserved_books,
        'form': form,
        'query': query,
    }

    return render(request, 'users/reserved_books_list.html', context)
