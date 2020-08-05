import pytest
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Populate the db with fixtures after setting it up.
    """
    with django_db_blocker.unblock():
        call_command("populatedb")
