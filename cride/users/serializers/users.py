from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from cride.users.models import User, Profile

from datetime import timedelta
import jwt

class UserModelSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = (
      'username',
      'first_name',
      'last_name',
      'email',
      'phone_number'
    )


class UserSignUpSerializer(serializers.Serializer):

  email = serializers.EmailField(
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  username = serializers.CharField(
    min_length=4,
    max_length=20,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  phone_regex = RegexValidator(
    regex=r'\+?1?\d{9,15}',
    message='Phone number must be entered in the format: +99999'
  )
  phone_number = serializers.CharField(validators=[phone_regex])
  password = serializers.CharField(min_length=8, max_length=64)
  password_confirmation = serializers.CharField(min_length=8, max_length=64)
  first_name = serializers.CharField(min_length=2, max_length=30)
  last_name = serializers.CharField(min_length=2, max_length=30)

  def validate(self, data):
    passwd = data['password']
    passwd_conf = data['password_confirmation']
    if passwd != passwd_conf:
      raise serializers.ValidationError('Passwords does not match')
    password_validation.validate_password(passwd)
    return data
  
  def create(self, data):
    data.pop('password_confirmation')
    user = User.objects.create_user(**data, is_verified=False)
    profile = Profile.objects.create(user=user)
    self.send_confirmation_email(user)
    return user
  
  def send_confirmation_email(self, user):
    verification_token = self.gen_verification_token(user)
    subject = 'welcome@{}! Veryfi your account'.format(user.username)
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    content = render_to_string('emails/users/account_verification.html', {'token': verification_token, 'user': user})
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, 'text/html')
    msg.send()


  def gen_verification_token(self, user):
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
      'user': user.username,
      'exp': int(exp_date.timestamp()),
      'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

class UserLoginSerializer(serializers.Serializer):
  
  email = serializers.EmailField()
  password = serializers.CharField(min_length=8, max_length=64)

  def validate(self, data):

    user = authenticate(username=data['email'], password=data['password'])
    if not user:
      raise serializers.ValidationError('Invalid credentials')
    if not user.is_verified:
      raise serializers.ValidationError('Account is not active yet')
    self.context['user'] = user
    return data

  def create(self, data):

    token, created = Token.objects.get_or_create(user=self.context['user'])
    return self.context['user'], token.key