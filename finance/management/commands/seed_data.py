import random
import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.db import transaction
from faker import Faker

# Assuming your Dues model is in the 'finance' app
from finance.models import Dues

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with fake data for testing.'

    def add_arguments(self, parser):
        parser.add_argument('--members', type=int, help='The number of members to create.', default=25)

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        # Be careful with deleting users. This deletes all non-superusers.
        # Adjust if you have other staff/special users to preserve.
        User.objects.filter(is_superuser=False).delete()
        Dues.objects.all().delete()

        # The 'en_GH' locale is not standard in the Faker library, causing an error.
        # We'll use 'en_GB' (Great Britain) as a close alternative.
        # For truly localized Ghanaian data, a custom provider would be needed.
        fake = Faker('en_GB')
        num_members = options['members']
        members = []

        self.stdout.write(f'Creating {num_members} new members...')
        for _ in range(num_members):
            member = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                # The CustomUser model uses email as the username.
                # Using fake.unique.email() prevents IntegrityError on duplicate emails.
                email=fake.unique.email(),
                # NOTE: Assuming your custom User model has these fields.
                # If not, you may need to adjust this part.
                staff_id=fake.unique.numerify(text='ST-####'),
                phone_number=fake.phone_number(),
                date_joined=fake.date_time_this_decade(tzinfo=None),
                last_login=fake.date_time_this_month(tzinfo=None)
            )
            member.set_password('testing123')
            members.append(member)

        User.objects.bulk_create(members)
        self.stdout.write('Members created. Now creating dues payments...')

        # Refresh members from DB to get their PKs
        all_members = User.objects.filter(is_superuser=False)
        dues_to_create = []
        for member in all_members:
            # Each member will have between 5 and 20 payments
            for _ in range(random.randint(5, 20)):
                payment_date = fake.date_between(start_date='-3y', end_date='today')
                # Since bulk_create bypasses the model's save() method, we generate
                # the receipt_number here, matching the logic in the Dues model.
                date_str = payment_date.strftime('%Y%m%d')
                unique_id_part = str(uuid.uuid4()).split('-')[0].upper()
                receipt_number = f"RCPT-{date_str}-{unique_id_part}"
                due = Dues(
                    member=member,
                    payment_date=payment_date,
                    # This was creating single large payments. Let's create more realistic
                    # smaller payments that align with the application's monthly limit of 10.00.
                    amount=Decimal(random.choice(['5.00', '10.00'])),
                    receipt_number=receipt_number,
                    notes=fake.sentence() if random.choice([True, False]) else ''
                )
                dues_to_create.append(due)

        Dues.objects.bulk_create(dues_to_create)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully populated the database with {num_members} members and {len(dues_to_create)} dues payments.'
        ))