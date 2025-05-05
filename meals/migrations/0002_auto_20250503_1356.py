from django.db import migrations

def add_default_categories(apps, schema_editor):
    Category = apps.get_model('meals', 'Category')
    for name in ['Breakfast', 'Lunch', 'Supper']:
        Category.objects.get_or_create(name=name)

class Migration(migrations.Migration):
    dependencies = [
        ('meals', '0001_initial'),  # Adjust based on your migrations
    ]

    operations = [
        migrations.RunPython(add_default_categories),
    ]
