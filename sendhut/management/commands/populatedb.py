from random import choice, shuffle
from django.core.management.base import BaseCommand, CommandError

from sendhut.stores.models import Item, Store
from sendhut.factory import (
    ImageFactory, UserFactory, OptionGroupFactory,
    CartFactory, GroupOrderFactory, OptionFactory,
    OrderFactory, create_orderlines,
)
from .load_menus import create_lagos_stores


ADMIN_PASSWORD = USER_PASSWORD = 'h3ll02018!'


def get_random_food_categories():
    n = choice(range(1, 4))
    categories = [k for k, _ in Item.FOOD_CATEGORIES]
    shuffle(categories)
    return categories[:n]


class Command(BaseCommand):
    help = 'Populates the database with dummy Sendhut data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating ADMIN user'))

        # raise CommandError()
        self.stdout.write(self.style.SUCCESS('Creating users'))
        UserFactory.create_batch(3, password=USER_PASSWORD)

        # create admin user
        self.stdout.write(self.style.SUCCESS('Creating admin user'))
        admin = UserFactory.create(email='hello@sendhut.com', username='admin')
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password(ADMIN_PASSWORD)
        admin.save()

        self.stdout.write(self.style.SUCCESS('DONE'))


# IDEA(yao):
# create_fixture(store, menu_config)
# menu_config = {menu_1: [category, n_items], menu_2: [category, n_items]}
