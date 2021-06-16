from django.shortcuts import render
from django.db import transaction
from django.forms.models import model_to_dict

# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from recipe_hub.models import *
from recipe_hub.serializers import *

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from datetime import datetime, timedelta, timezone

import json

serverTZ = timezone(timedelta(hours=0), 'JST')


# @transaction.atomic
@swagger_auto_schema(methods=['post'], request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id_user': openapi.Schema(type=openapi.TYPE_STRING, description='user id'),
        'id_repo': openapi.Schema(type=openapi.TYPE_STRING, description='repository id'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='forked repository name')
    }),
    responses={201: 'Forked', 400: 'Bad Request'})
@api_view(['POST'])
def fork(request):
  """
  ---
  parameters:
  - name: id_user
    type: string
    required: true
    location: form
  - name: id_repo
    type: string
    required: true
    location: form
  - name: name
    type: string
    required: true
    location: form
  """
  data = json.loads(request.body)

  id_user = data['id_user']
  id_repo = data['id_repo']
  name = data['name']

  mRepo = MRepository.objects.filter(id=id_repo)

  if len(mRepo) != 1:
    raise ValueError('Illegal Argument: id_repo is not unique')

  mRepo = mRepo[0]

  mRepoObj = {}
  mRepoObj['id_author'] = id_user
  mRepoObj['id_fork_from'] = id_repo
  mRepoObj['name'] = name
  mRepoObj['recipe'] = mRepo.recipe

  mRepoSerializer = MRepositorySerializer(data=mRepoObj)

  if mRepoSerializer.is_valid(raise_exception=True):
    print(mRepoSerializer.errors)
    mRepoSerializer.save()
  else:
    return Response(mRepoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

  return Response({'status': 'created'}, status=status.HTTP_201_CREATED)