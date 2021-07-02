from rest_framework import serializers
from recipe_hub.models import *
from django.contrib.auth.hashers import make_password
from django.core.serializers.python import Serializer

class MySerialiser(Serializer):
  def end_object(self, obj):
    self._current['id'] = obj._get_pk_val()
    self.objects.append(self._current)

class MRepositorySerializer(serializers.ModelSerializer):
  class Meta:
    model = MRepository
    fields = '__all__'

class MImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = MImage
    fields = '__all__'

class MUserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
      write_only=True,
      required=True,
      style={'input_type': 'password', 'placeholder': 'Password'}
  )

  class Meta:
    model = MUser
    fields = '__all__'

  def create(self, validated_data):
    validated_data['password'] = make_password(validated_data.get('password'))

    return super(MUserSerializer, self).create(validated_data)

