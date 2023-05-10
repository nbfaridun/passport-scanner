from django.core.management.base import BaseCommand
from .models import Passport
import json

class Command(BaseCommand):
    help = 'Load data from JSON file to PostgreSQL'

    def handle(self, *args, **options):
        with open('data.json', 'r') as f:
            data = json.load(f)

        for passport_data in data:
            passport = Passport(
                type=passport_data['Type'],
                issuing_country=passport_data['Issuing Country'],
                surname=passport_data['Surname'],
                name=passport_data['Name'],
                passport_number=passport_data['Passport Number'],
                nationality=passport_data['Nationality'],
                dob=passport_data['DOB'],
                sex=passport_data['Sex'],
                doe=passport_data['DOE']
            )
            passport.save()