# listings/serializers.py
from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['review_id', 'listing', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['review_id', 'created_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class BookingSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'booking_id', 'listing', 'user',
            'start_date', 'end_date', 'total_price',
            'status', 'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at', 'status']

class ListingSerializer(serializers.ModelSerializer):
    host = UserSimpleSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = [
            'listing_id', 'title', 'description', 'address',
            'host', 'price_per_night', 'created_at', 'reviews', 'bookings'
        ]
        read_only_fields = ['listing_id', 'created_at', 'host']
