# users/views.py
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# views.py
from rest_framework import generics
from library.models.book import Book
from api_app.serializers import BookSerializer
from .serializers import LoginSerializer
from library.models.reserve_book import ReserveBook
from api_app.serializers import ReserveBookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from library.models.book import Book
from library.models.issued_book import IssuedBook
from .serializers import BookSerializer, IssuedBookSerializer
from django.utils import timezone
from datetime import timedelta


class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReserveBookCreate(generics.CreateAPIView):
    queryset = ReserveBook.objects.all()
    serializer_class = ReserveBookSerializer


class ReserveBookList(generics.ListAPIView):
    queryset = ReserveBook.objects.all()
    serializer_class = ReserveBookSerializer


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