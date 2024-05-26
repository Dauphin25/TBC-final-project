from django.urls import path

from api_app import views
from api_app.views import LoginAPIView, BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView, DashboardAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path('reservations/', views.ReserveBookCreate.as_view(), name='reservation-create'),
    path('reservations/list/', views.ReserveBookList.as_view(), name='reservation-list'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard_api'),
]
