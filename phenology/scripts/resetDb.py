from backend.sampledb import create_sample_data
from django.core.management.sql import sql_delete


def run():
    create_sample_data()

