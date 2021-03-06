from django.core.management.base import BaseCommand

from sendhut.envoy import DeliveryStatus
from sendhut.payments import TransactionTypes
from sendhut.factory import (
    DeliveryFactory, UserFactory, TransactionFactory
)


ADMIN_PASSWORD = USER_PASSWORD = 'h3ll02018!'


class Command(BaseCommand):
    help = 'Populates the database with dummy Sendhut data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating ADMIN user'))

        self._create_deliveries()

        # create admin user
        self.stdout.write(self.style.SUCCESS('Creating admin user'))
        admin = UserFactory.create(email='hello@sendhut.com', username='admin')
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password(ADMIN_PASSWORD)
        admin.save()
        self._create_deliveries([admin])

        # setup wallets
        for user in UserFactory.Meta.model.objects.all():
            self._setup_wallet(user)

        self.stdout.write(self.style.SUCCESS('DONE'))

    def _create_deliveries(self, users=None):
        self.stdout.write(self.style.SUCCESS('Creating users'))
        users = users or UserFactory.create_batch(3, password=USER_PASSWORD)
        for user in users:
            DeliveryFactory.create_batch(1, user=user)
            DeliveryFactory.create_batch(2, status=DeliveryStatus.DELIVERED, user=user)
            DeliveryFactory.create_batch(5, status=DeliveryStatus.SCHEDULED, user=user)
            DeliveryFactory.create_batch(10, user=user)

    def _setup_wallet(self, user):
        TransactionFactory.create_batch(
            10, wallet=user.service_wallet,
            txn_type=TransactionTypes.LOAD_WALLET)

        TransactionFactory.create_batch(
            3, wallet=user.service_wallet,
            txn_type=TransactionTypes.WALLET_PAYMENT)
