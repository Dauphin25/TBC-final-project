from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from library.models.reserve_book import ReserveBook
from api_app.serializers import ReserveBookSerializer
from users.forms import UpdateIsTakenForm


class ReservedBooksListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q')

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

        active_reserved_books_serializer = ReserveBookSerializer(active_reserved_books, many=True)
        canceled_reserved_books_serializer = ReserveBookSerializer(canceled_reserved_books, many=True)
        taken_reserved_books_serializer = ReserveBookSerializer(taken_reserved_books, many=True)

        return Response({
            'active_reserved_books': active_reserved_books_serializer.data,
            'canceled_reserved_books': canceled_reserved_books_serializer.data,
            'taken_reserved_books': taken_reserved_books_serializer.data,
            'query': query,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        form = UpdateIsTakenForm(request.data)
        if form.is_valid():
            reservation_id = request.data.get('reservation_id')
            reservation = get_object_or_404(ReserveBook, id=reservation_id)
            reservation.is_taken = form.cleaned_data['is_taken']
            reservation.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReservedBooksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.GET.get('q', '')
        sort_order = request.GET.get('sort', 'newest')

        user = request.user.library_user
        active_reserved_books = ReserveBook.objects.filter(user=user, is_taken=False, status='active')
        canceled_reserved_books = ReserveBook.objects.filter(user=user, status='canceled')
        history_reserved_books = ReserveBook.objects.filter(user=user, is_taken=True)

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

        active_reserved_books_serializer = ReserveBookSerializer(active_reserved_books, many=True)
        canceled_reserved_books_serializer = ReserveBookSerializer(canceled_reserved_books, many=True)
        history_reserved_books_serializer = ReserveBookSerializer(history_reserved_books, many=True)

        return Response({
            'active_reserved_books': active_reserved_books_serializer.data,
            'canceled_reserved_books': canceled_reserved_books_serializer.data,
            'history_reserved_books': history_reserved_books_serializer.data,
            'search_query': search_query,
            'sort_order': sort_order
        }, status=status.HTTP_200_OK)
