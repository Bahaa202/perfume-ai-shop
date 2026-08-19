from app import app
from models import db, Product

sample_products = [
    {
        "name": "Oud Royale",
        "brand": "Al Majd",
        "description": "A rich, warm oud fragrance with notes of amber and sandalwood. Perfect for evening wear and special occasions. Long-lasting projection.",
        "price": 89.99,
        "category": "evening",
        "stock": 25,
    },
    {
        "name": "Citrus Breeze",
        "brand": "Al Majd",
        "description": "A light, fresh citrus scent with notes of bergamot and lemon. Ideal for daily wear, office, and summer days.",
        "price": 39.99,
        "category": "daily",
        "stock": 60,
    },
    {
        "name": "Rose Noir",
        "brand": "Zahra Perfumes",
        "description": "An elegant floral fragrance combining Bulgarian rose with dark musk. Great for evening events and romantic occasions.",
        "price": 74.50,
        "category": "evening",
        "stock": 18,
    },
    {
        "name": "Desert Wind",
        "brand": "Zahra Perfumes",
        "description": "A woody oud-based scent with hints of leather and spice. Bold and long-lasting, suited for formal evening gatherings.",
        "price": 95.00,
        "category": "oud",
        "stock": 12,
    },
    {
        "name": "Morning Jasmine",
        "brand": "Al Majd",
        "description": "A soft floral fragrance with jasmine and white musk. Light enough for daily use and office environments.",
        "price": 45.00,
        "category": "daily",
        "stock": 40,
    },
    {
        "name": "Amber Nights",
        "brand": "Zahra Perfumes",
        "description": "A deep amber and vanilla blend, warm and sensual. Best worn in the evening or during cold weather.",
        "price": 68.00,
        "category": "evening",
        "stock": 22,
    },
]

with app.app_context():
    db.create_all()
    for item in sample_products:
        product = Product(**item)
        db.session.add(product)
    db.session.commit()
    print(f"Seeded {len(sample_products)} products successfully.")
