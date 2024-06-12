# users/views.py
from django.db import models
from api_app.serializers import IssuedBookSerializer
from library.models.issued_book import IssuedBook
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from library.models.book import Book
from library.models.author import Author
from api_app.serializers import AuthorSerializer, BookSerializer

class HomeAPIView(APIView):
    def get(self, request):
        # Fetch necessary data from the database
        user_info = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        } if request.user.is_authenticated else None

        news = "Welcome to our library! Check out our latest collections and upcoming events."

        # Fetch the 3 most popular authors
        popular_authors = Author.objects.annotate(num_books=Count('book')).order_by('-num_books')[:3]
        popular_authors_serializer = AuthorSerializer(popular_authors, many=True)

        # Fetch the 5 most popular books by number of borrows
        popular_books = Book.objects.order_by('-borrowed_quantity')[:5]
        popular_books_serializer = BookSerializer(popular_books, many=True)

        # Prepare the response data
        data = {
            'user_info': user_info,
            'news': news,
            'popular_authors': popular_authors_serializer.data,
            'popular_books': popular_books_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)


class DashboardAPIView(APIView):
    def get(self, request, format=None):
        # 10 most popular books (borrowed most times in the last year)
        one_year_ago = timezone.now() - timedelta(days=365)

        popular_books = Book.objects.filter(
            issuedbook__issued_date__gte=one_year_ago
        ).annotate(
            borrowed_count=models.Count('issuedbook')
        ).order_by('-borrowed_count')[:10]

        # Top 100 books returned lately
        lately_returned_books = IssuedBook.objects.filter(
            return_date__isnull=False
        ).order_by('-return_date')[:100]

        # Top 100 users who were late in returning books
        top_late_users = IssuedBook.objects.filter(
            return_date__isnull=False
        ).annotate(
            delay=models.ExpressionWrapper(
                models.F('return_date') - models.F('due_date'),
                output_field=models.DurationField()
            )
        ).order_by('-delay')[:100]

        # Serialize data
        popular_books_data = BookSerializer(popular_books, many=True).data
        lately_returned_books_data = IssuedBookSerializer(lately_returned_books, many=True).data
        top_late_users_data = IssuedBookSerializer(top_late_users, many=True).data

        response_data = {
            'popular_books': popular_books_data,
            'lately_returned_books': lately_returned_books_data,
            'top_late_users': top_late_users_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
