from django.db import models
from django.contrib.auth.models import AbstracUser

from cride.utils.models import CRideModel

class User(CRideModel, AbstracUser):
  email = models.EmailField(
    'email address',
    unique=True,
    error_message={
      'unique': 'A user with that email already exists.'
    }
  )
  phone_number = models.CharField(max_length=17, blanck=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  is_client = models.BooleanField(
    'client',
    default=True,
    help_text=(
      'Help easily distinguish users and perform queries.'
      'Clients are the main type of user.'
    )
  )

  is_verified = models.BooleanField(
    'verified',
    default=True,
    help_text='Set to true when the user have verified its email address'
  )