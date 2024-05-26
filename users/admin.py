from django.contrib import admin
from users.models.library_user import LibraryUser
from users.models.librarian import Librarian


@admin.register(LibraryUser)
class LibraryUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    pass