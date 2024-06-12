from django.urls import path
from api_app.views.login import LoginAPIView
from api_app.views.book import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView,  \
    ReserveBookList, ReserveBookAPIView
from api_app.views.statistics import DashboardAPIView, HomeAPIView
from rest_framework import permissions
from api_app.views.users import UserReservedBooksAPIView, ReservedBooksListAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="API documentation for the library system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('home/', HomeAPIView.as_view(), name='home_api'),
    path('reserve_book/<int:pk>/', ReserveBookAPIView.as_view(), name='reserve_book_api'),
    path('user-reserved-books/', UserReservedBooksAPIView.as_view(), name='user_reserved_books_api'),
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('update-reserved-books/', ReservedBooksListAPIView.as_view(), name='update-reserved_books_list_api'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path('reservations/list/', ReserveBookList.as_view(), name='reservation-list'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard_api'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
