
from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from faker import Faker

from rental.contract.models import Contract
from rental.notes.models import Note

fake = Faker()

User = get_user_model()


class NoteMixin:
    def create_note(self, user: User, contract: Contract):
        with set_actor(user):
            return Note.objects.create(
                user=user,
                contract=contract,
                subject=fake.text(max_nb_chars=30),
                body=fake.sentence(nb_words=10),
            )
