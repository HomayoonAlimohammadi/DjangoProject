import os
from django.test import TestCase
# or do this for getting secret key
from django.conf import settings
from django.contrib.auth.password_validation import validate_password


class TryDjangoConfigTest(TestCase):
    # all the methods have to start with test_<anything> 
    # Checkout python unittest > TestCase for more info
    def test_secret_key_strength(self):
        # get the secret key
        SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
        # another way: SECRET_KEY = settings.SECRET_KEY
        # how to make sure the password is good?
        try:
            is_strong = validate_password(SECRET_KEY)
        except Exception as e:
            msg = f'Weak SECRET_KEY {e.messages}'
            self.fail(msg) # what message to fail with

    