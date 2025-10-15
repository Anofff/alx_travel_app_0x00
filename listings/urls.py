# listings/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ListingViewSet, BookingViewSet, ReviewViewSet

router = DefaultRouter()
router.register('listings', ListingViewSet, basename='listings')
router.register('bookings', BookingViewSet, basename='bookings')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
