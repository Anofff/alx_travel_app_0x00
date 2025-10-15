# listings/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from django_seed import Seed
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with listings, bookings and reviews."

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=5, help='Number of users to create')
        parser.add_argument('--listings', type=int, default=10, help='Number of listings to create')

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        users_count = options['users']
        listings_count = options['listings']

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
        def create_listing():
            host = random.choice(users)
            title = seeder.faker.sentence(nb_words=4)
            description = seeder.faker.paragraph(nb_sentences=3)
            address = seeder.faker.address()
            price = round(random.uniform(25.0, 500.0), 2)
            return {
                'title': title,
                'description': description,
                'address': address,
                'host': host,
                'price_per_night': price
            }

        for _ in range(listings_count):
            data = create_listing()
            listing = Listing.objects.create(**data)
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
                    comment=seeder.faker.sentence(nb_words=10)
                )

        self.stdout.write(self.style.SUCCESS(f"Seeded {listings_count} listings with bookings and reviews."))
