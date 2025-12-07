# Run with: python manage.py shell < scripts/load_sample_data.py
from products.models import Product
Product.objects.create(name='Sample A', sku='SAMP-A', price=10000, stock=10)
Product.objects.create(name='Sample B', sku='SAMP-B', price=20000, stock=5)
print('Sample products created')
