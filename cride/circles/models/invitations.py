from django.db import models

from cride.utils.models import CRideModel

from cride.circles.managers import InvitationManager

class Invitation(CRideModel):

  code = models.CharField(max_length=50, unique=True)

  issued_by = models.ForeignKey(
    'users.User',
    on_delete=models.CASCADE,
    help_text='Circle member provider invitation',
    related_name='issued_by'
  )
  used_by = models.ForeignKey(
    'users.User',
    on_delete=models.CASCADE,
    null=True,
    help_text='User that used the code to enter the circle'
  )
  
  circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

  used = models.BooleanField(default=False)
  used_at = models.DateTimeField(blank=True, null=True)

  objects = InvitationManager()

  def __str__(self):
    return '#{}: {}'.format(self.circle.slug_name, self.code)
