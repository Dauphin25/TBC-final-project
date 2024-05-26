from django.contrib import admin
from library.models.author import Author
from library.models.book import Book
from library.models.genre import Genre
from library.models.publisher import Publisher
from library.models.tags import Tag
from library.models.reserve_book import ReserveBook
from library.models.issued_book import IssuedBook


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'country', 'birth_date', 'death_date')
    search_fields = ('first_name', 'last_name', 'country')
    list_filter = ('country', 'birth_date', 'death_date')
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'birth_date'
    empty_value_display = '-empty-'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'published_date', 'stock_quantity', 'borrowed_quantity', 'current_borrowed_quantity', 'currently_available_quantity')
    search_fields = ('title', 'author', 'publisher', 'published_date', 'stock_quantity', 'borrowed_quantity', 'current_borrowed_quantity', 'currently_available_quantity')
    list_filter = ('published_date', 'stock_quantity', 'borrowed_quantity', 'current_borrowed_quantity', 'currently_available_quantity')
    date_hierarchy = 'published_date'
    empty_value_display = '-empty-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'email', 'website')
    search_fields = ('name', 'country', 'city', 'email', 'website')
    list_filter = ('country', 'city')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ReserveBook)
class ReserveBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'reserved_date', 'take_date', 'due_date', 'is_taken')
    search_fields = ('book', 'user')
    list_filter = ('reserved_date', 'take_date', 'due_date', 'is_taken')
    date_hierarchy = 'reserved_date'
    empty_value_display = '-empty-'


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'issued_date', 'due_date', 'returned', 'return_date')
    search_fields = ('book', 'user')
    list_filter = ('issued_date', 'due_date', 'returned', 'return_date')
    date_hierarchy = 'issued_date'
    empty_value_display = '-empty-'

