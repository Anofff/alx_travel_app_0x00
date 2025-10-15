# ALX Travel App

A Django REST API travel application that allows users to browse listings, make bookings, and leave reviews.

## Features

- **Listings Management**: Create and manage travel property listings
- **Booking System**: Users can book listings with date ranges and pricing
- **Review System**: Users can rate and review listings
- **REST API**: Full REST API with Django REST Framework
- **Admin Interface**: Django admin interface for managing data

## Models

### Listing
- Property listings with title, description, address, and pricing
- Linked to host (user) who created the listing
- UUID primary key for security

### Booking
- Booking system with start/end dates
- Status tracking (pending, confirmed, canceled)
- Total price calculation
- Linked to listing and user

### Review
- Rating system (1-5 stars)
- Comment functionality
- Linked to listing and user

## API Endpoints

- `GET /api/listings/` - List all listings
- `GET /api/listings/{id}/` - Get specific listing
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create new review

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Anofff/alx_travel_app_0x00.git
cd alx_travel_app_0x00
```

2. Install dependencies:
```bash
pip install django djangorestframework django-seed psycopg2-binary
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Seed the database:
```bash
python manage.py seed
```

6. Run the development server:
```bash
python manage.py runserver
```

## Database Seeding

The project includes a management command to populate the database with sample data:

```bash
# Default: 5 users, 10 listings
python manage.py seed

# Custom amounts
python manage.py seed --users 10 --listings 20
```

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to manage:
- Listings
- Bookings
- Reviews
- Users

## Technologies Used

- Django 5.2
- Django REST Framework
- SQLite (development)
- UUID for primary keys
- Django-seed for test data generation

## Project Structure

```
alx_travel_app_0x00/
├── alx_travel_app/          # Django project settings
├── listings/                # Main app
│   ├── models.py           # Database models
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views
│   ├── urls.py             # URL routing
│   └── management/
│       └── commands/
│           └── seed.py     # Database seeding command
├── manage.py               # Django management script
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the ALX curriculum.