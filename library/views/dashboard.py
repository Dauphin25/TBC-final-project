# views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F, ExpressionWrapper, fields
from django.shortcuts import render
from datetime import datetime, timedelta
from library.models.book import Book
from library.models.issued_book import IssuedBook


@login_required
def dashboard(request):
    # Calculate the date one year ago from today
    one_year_ago = datetime.now() - timedelta(days=365)

    # 10 most popular books based on borrowed count in the last year
    popular_books = Book.objects.annotate(
        borrowed_count=Count('issuedbook', filter=Q(issuedbook__issued_date__gte=one_year_ago))
    ).order_by('-borrowed_count')[:10]

    # Top 100 books which were returned lately
    lately_returned_books = IssuedBook.objects.filter(
        returned=True
    ).order_by('-return_date')[:100]

    # Top 100 users who were late in returning books
    top_late_users = IssuedBook.objects.filter(
        returned=True,
        return_date__gt=F('due_date')
    ).annotate(
        delay=ExpressionWrapper(F('return_date') - F('due_date'), output_field=fields.DurationField())
    ).order_by('-delay')[:100]

    context = {
        'popular_books': popular_books,
        'lately_returned_books': lately_returned_books,
        'top_late_users': top_late_users,
    }
    print(popular_books, lately_returned_books, top_late_users)
    print("fsdvbs")

    return render(request, 'library/dashboard.html', context)
