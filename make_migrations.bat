@echo off
echo Creating migrations for topshiriq app...
python manage.py makemigrations topshiriq

echo Applying migrations...
python manage.py migrate

echo Checking for any remaining migrations...
python manage.py makemigrations

echo Applying any remaining migrations...
python manage.py migrate

echo Creating superuser if needed...
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo Database setup complete!
pause
