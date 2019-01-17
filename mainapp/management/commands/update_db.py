from django.core.management.base import BaseCommand
from accounts.models import Account
from accounts.models import AccountProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = Account.objects.all()
        for user in users:
            users_profile = AccountProfile.objects.create(user=user)
            users_profile.save()
