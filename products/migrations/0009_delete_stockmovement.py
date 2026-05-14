# Generated manually

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_products_stock'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StockMovement',
        ),
    ]
