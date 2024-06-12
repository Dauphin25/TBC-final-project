# users/serializers.py
# serializers.py
from rest_framework import serializers
from library.models import IssuedBook
from library.models.author import Author
from library.models.book import Book
from library.models.reserve_book import ReserveBook
from users.models.library_user import LibraryUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ReserveBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = ReserveBook
        fields = '__all__'


class IssuedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedBook
        fields = '__all__'  # Serialize all fields of the IssuedBook model


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'  # Serialize all fields of the Author model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = '__all__'  # Serialize all fields of the User model


class TopBookSerializer(serializers.Serializer):
    title = serializers.CharField()
    borrowed_count = serializers.IntegerField()


class TopAuthorSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    total_books = serializers.IntegerField()


class TopUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    total_delay = serializers.DurationField()


class DashboardSerializer(serializers.Serializer):
    total_books = serializers.IntegerField()
    total_borrowed_books = serializers.IntegerField()
    total_available_books = serializers.IntegerField()
    average_delay = serializers.DurationField()
    top_books = TopBookSerializer(many=True)
    top_authors = TopAuthorSerializer(many=True)
    top_users = TopUserSerializer(many=True)
    reserved_books = serializers.IntegerField()
    total_active_users = serializers.IntegerField()



