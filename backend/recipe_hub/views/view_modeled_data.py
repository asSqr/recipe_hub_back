from django.shortcuts import render
from django.db import transaction
from django.forms.models import model_to_dict

# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from recipe_hub.models import *
from recipe_hub.serializers import *

class MUserViewSet(ModelViewSet):
  serializer_class = MUserSerializer
  queryset = MUser.objects.all()

class MRepositoryViewSet(ModelViewSet):
  serializer_class = MRepositorySerializer
  queryset = MRepository.objects.all()

class MImageViewSet(ModelViewSet):
  serializer_class = MImageSerializer
  queryset = MImage.objects.all()