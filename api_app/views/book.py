
from api_app.serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from library.models.book import Book
from library.models.reserve_book import ReserveBook
from users.models.library_user import LibraryUser
from api_app.serializers import ReserveBookSerializer
from django.utils import timezone


class BookPagination(PageNumberPagination):
    page_size = 10


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination


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


class ReserveBookList(generics.ListAPIView):
    queryset = ReserveBook.objects.all()
    serializer_class = ReserveBookSerializer


class ReserveBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        user = get_object_or_404(LibraryUser, user=request.user)

        # Check if a reservation already exists for this user and book
        if ReserveBook.objects.filter(book=book, user=user, status='active').exists():
            return Response({'error': 'You have already reserved this book.'}, status=status.HTTP_400_BAD_REQUEST)

        if book.currently_available_quantity > 0:
            reserve = ReserveBook(
                book=book,
                user=user,
                reserved_date=timezone.now(),
                due_date=timezone.now() + timezone.timedelta(days=1)
            )
            reserve.save()
            book.currently_available_quantity -= 1
            book.save()
            return Response({'success': 'Book reserved successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Sorry, this book is currently not available for reservation.'}, status=status.HTTP_400_BAD_REQUEST)