from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField, Sum
from django.shortcuts import render
from library.models.book import Book
from library.models.issued_book import IssuedBook
from library.models.reserve_book import ReserveBook
from library.models.author import Author
from users.models.library_user import LibraryUser


def dashboard(request):
    one_year_ago = timezone.now() - timedelta(days=365)
    one_month_ago = timezone.now() - timedelta(days=30)

    # Total statistics
    total_books = Book.objects.count()
    total_borrowed_books = IssuedBook.objects.filter(returned=False).count()
    total_available_books = Book.objects.aggregate(total_available=Sum('currently_available_quantity'))['total_available']
    reserved_books = ReserveBook.objects.filter(reserved_date__gte=one_month_ago).count()
    total_active_users = LibraryUser.objects.count()

    # Average delay in returning books
    average_delay = IssuedBook.objects.filter(return_date__isnull=False).annotate(
        delay=ExpressionWrapper(F('return_date') - F('due_date'), output_field=DurationField())
    ).aggregate(average_delay=Avg('delay'))['average_delay']

    # Top books (most borrowed)
    top_books = Book.objects.annotate(borrowed_count=Count('issuedbook')).order_by('-borrowed_count')[:5]

    # Top authors (most books published)
    top_authors = Author.objects.annotate(total_books=Count('book')).order_by('-total_books')[:3]

    reserved_books = ReserveBook.objects.filter(reserved_date__gte=one_month_ago).count()
    total_active_users = LibraryUser.objects.count()

    # Top users (most late returns)
    top_users = IssuedBook.objects.filter(return_date__isnull=False).annotate(
        delay=ExpressionWrapper(F('return_date') - F('due_date'), output_field=DurationField())
    ).values('user__first_name', 'user__last_name').annotate(
        total_delay=Avg('delay')
    ).order_by('-total_delay')[:3]

    context = {
        'total_books': total_books,
        'total_borrowed_books': total_borrowed_books,
        'total_available_books': total_available_books,
        'average_delay': average_delay,
        'top_books': top_books,
        'top_authors': top_authors,
        'top_users': top_users,
        'reserved_books': reserved_books,
        'total_active_users': total_active_users,
    }
    return render(request, 'library/dashboard.html', context)
