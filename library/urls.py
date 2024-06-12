from library.views.home import home
from django.urls import path
from library.views.book import BookListView, BookDetailView, ReserveBookView
from library.views.author import AuthorListView, AuthorDetailView
from django.conf import settings
from django.conf.urls.static import static
from library.views.dashboard import dashboard

urlpatterns = [
    path('', home, name='home'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('books/<int:pk>/reserve/', ReserveBookView.as_view(), name='reserve_book'),
    path('dashboard/', dashboard, name='dashboard'),

]
# Add the following line to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)