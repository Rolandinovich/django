from django.core.management.base import BaseCommand
from mainapp.models import Category
import json, os

JSON_PATH = 'data'


def loadFromJSON(file_name):
     with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding="utf-8") as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = loadFromJSON('categorys')
        print(categories)

        Category.objects.all().delete()
        for category in categories['Categories']:
            new_category = Category(**category)
            new_category.save()
