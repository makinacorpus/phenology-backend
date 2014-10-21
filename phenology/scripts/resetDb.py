from backend.sampledb import create_sample_data
from django.contrib.auth.models import User


def run():
    User.objects.create_superuser(username='admin',
                                  email='admin@admin.fr',
                                  password='admin')
    create_sample_data()
