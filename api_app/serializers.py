# users/serializers.py
# serializers.py
from rest_framework import serializers

from library.models import IssuedBook
from library.models.book import Book
from library.models.reserve_book import ReserveBook


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ReserveBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveBook
        fields = '__all__'


class IssuedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedBook
        fields = '__all__'  # Serialize all fields of the IssuedBook model
