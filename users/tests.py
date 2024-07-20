import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username="testuser", password="testpassword")
    assert user.username == "testuser"
