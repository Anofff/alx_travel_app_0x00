# listings/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with listings, bookings and reviews."

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=5, help='Number of users to create')
        parser.add_argument('--listings', type=int, default=10, help='Number of listings to create')

    def handle(self, *args, **options):
        users_count = options['users']
        listings_count = options['listings']

        # Sample data for realistic content
        sample_titles = [
            "Cozy Beachfront Villa", "Modern Downtown Apartment", "Charming Mountain Cabin",
            "Luxury City Penthouse", "Rustic Country House", "Stylish Urban Loft",
            "Traditional Family Home", "Contemporary Studio", "Historic Townhouse",
            "Seaside Bungalow", "Garden View Apartment", "Skyline Penthouse"
        ]
        
        sample_descriptions = [
            "A beautiful and comfortable space perfect for your vacation.",
            "Modern amenities with stunning views and convenient location.",
            "Charming property with character and all the comforts of home.",
            "Luxury accommodation with premium facilities and services.",
            "Peaceful retreat in a prime location with excellent amenities.",
            "Stylish and contemporary space designed for relaxation and comfort."
        ]
        
        sample_addresses = [
            "123 Ocean Drive, Miami, FL 33139", "456 Main Street, New York, NY 10001",
            "789 Mountain View Road, Denver, CO 80202", "321 Park Avenue, Los Angeles, CA 90210",
            "654 Sunset Boulevard, San Francisco, CA 94102", "987 Broadway, Seattle, WA 98101"
        ]
        
        sample_comments = [
            "Great place to stay, highly recommended!", "Perfect location and excellent amenities.",
            "Clean and comfortable, would definitely stay again.", "Beautiful property with amazing views.",
            "Excellent host and wonderful accommodation.", "Fantastic experience, exceeded expectations."
        ]

        # create a few users if not present
        existing_users = User.objects.count()
        if existing_users < users_count:
            for i in range(users_count - existing_users):
                User.objects.create_user(
                    username=f'user{i+existing_users+1}',
                    email=f'user{i+existing_users+1}@example.com',
                    password='password123'
                )
            self.stdout.write(self.style.SUCCESS(f'Created {users_count - existing_users} users.'))

        users = list(User.objects.all())

        # seed listings
        for i in range(listings_count):
            host = random.choice(users)
            title = random.choice(sample_titles) + f" #{i+1}"
            description = random.choice(sample_descriptions)
            address = random.choice(sample_addresses)
            price = round(random.uniform(25.0, 500.0), 2)
            
            listing = Listing.objects.create(
                title=title,
                description=description,
                address=address,
                host=host,
                price_per_night=price
            )
            
            # add bookings and reviews
            # create 0-3 bookings
            for _ in range(random.randint(0, 3)):
                user = random.choice(users)
                start = date.today() + timedelta(days=random.randint(1, 30))
                end = start + timedelta(days=random.randint(1, 7))
                nights = (end - start).days
                total_price = round(listing.price_per_night * nights, 2)
                Booking.objects.create(
                    listing=listing,
                    user=user,
                    start_date=start,
                    end_date=end,
                    total_price=total_price,
                    status=random.choice([Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED, Booking.STATUS_CANCELED])
                )
            
            # create 0-5 reviews
            for _ in range(random.randint(0, 5)):
                user = random.choice(users)
                Review.objects.create(
                    listing=listing,
                    user=user,
                    rating=random.randint(1, 5),
                    comment=random.choice(sample_comments)
                )

        self.stdout.write(self.style.SUCCESS(f"Seeded {listings_count} listings with bookings and reviews."))