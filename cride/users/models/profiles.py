from django.db import models
from cride.utils.models import CRideModel

class Profile(CRideModel):
  user = models.OneToOneField('users.User', on_delete=models.CASCADE)

  picture = models.ImageField(
    'profile picture',
    upload_to='users/pictures/',
    blank=True,
    null=True
  )

  biography = models.TextField(max_length=500, blank=True)

  rides_taken = models.PositiveIntegerField(default=0)
  rides_offered = models.PositiveIntegerField(default=0)
  reputation = models.FloatField(
    default=5.0,
    help_text='User reputation'
  )

  def __srt__(self):
    return str(self.user)