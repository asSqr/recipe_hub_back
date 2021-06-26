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
import os
import sys

serverTZ = timezone(timedelta(hours=0), 'JST')

sys.setrecursionlimit(1500)

@transaction.atomic
@swagger_auto_schema(methods=['post'], request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id_user': openapi.Schema(type=openapi.TYPE_STRING, description='user id'),
        'id_repo': openapi.Schema(type=openapi.TYPE_STRING, description='repository id'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='forked repository name'),
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='forked repository title'),
        'recipe': openapi.Schema(type=openapi.TYPE_STRING, description='forked repository recipe'),
        'genre': openapi.Schema(type=openapi.TYPE_STRING, description='forked repository genre'),
        'thumbnail': openapi.Schema(type=openapi.TYPE_FILE, description='forked repository thumbnail')
    }),
    responses={201: 'Forked', 400: 'Bad Request'})
@api_view(['POST'])
def fork(request):
  data = json.loads(request.body)

  id_user = data['id_user']
  id_repo = data['id_repo']
  name = data['name']
  title = data['title']
  recipe = data['recipe']
  genre = data['genre']
  thumbnail = data['thumbnail']

  mRepo = MRepository.objects.filter(id=id_repo)

  if len(mRepo) != 1:
    raise ValueError('Illegal Argument: id_repo is not unique')

  mRepo = mRepo[0]

  mRepoObj = {}
  mRepoObj['id_author'] = id_user
  mRepoObj['id_fork_from'] = id_repo
  mRepoObj['name'] = name
  mRepoObj['title'] = title
  mRepoObj['recipe'] = recipe
  mRepoObj['genre'] = genre
  mRepoObj['thumbnail'] = thumbnail

  mRepoSerializer = MRepositorySerializer(data=mRepoObj)

  if mRepoSerializer.is_valid(raise_exception=True):
    print(mRepoSerializer.errors)
    newMRepo = mRepoSerializer.save()
  else:
    return Response(mRepoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

  fork_to_list = json.loads(mRepo.id_fork_to_list)

  if 'list' in fork_to_list:
    fork_to_list['list'].append(str(newMRepo.id))
  else:
    fork_to_list['list'] = [str(newMRepo.id)]

  mRepoObj = {}
  mRepoObj['id_fork_to_list'] = json.dumps(fork_to_list)

  mRepoSerializer = MRepositorySerializer(mRepo, data=mRepoObj, partial=True)

  if mRepoSerializer.is_valid(raise_exception=True):
    print(mRepoSerializer.errors)
    mRepoSerializer.save()
  else:
    return Response(mRepoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

  return Response({'status': 'created'}, status=status.HTTP_201_CREATED)

def fetch_repo(id_repo):
  mRepo = MRepository.objects.filter(id=id_repo)

  if len(mRepo) != 1:
    raise ValueError('Illegal Argument: id_repo is not unique')

  return mRepo[0]

def mk_tree(mRepo):
  fork_list = json.loads(mRepo.id_fork_to_list)

  ret = {}

  children = []

  if 'list' in fork_list:
    for id_repo in fork_list['list']:
      children.append(mk_tree(fetch_repo(id_repo)))

  base_url = os.getenv('API_URL') if os.getenv('API_URL') is not None else 'http://localhost:8000'

  ret['id'] = str(mRepo.id)
  ret['title'] = mRepo.title
  ret['name'] = mRepo.name
  ret['recipe'] = mRepo.recipe
  ret['genre'] = mRepo.genre
  ret['id_author'] = mRepo.id_author
  if mRepo.thumbnail:
    ret['thumbnail'] = base_url + str(mRepo.thumbnail.url)
  ret['create_date'] = mRepo.create_date
  ret['update_date'] = mRepo.update_date
  ret['next'] = children

  return ret

@transaction.atomic
@swagger_auto_schema(methods=['get'], response_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
      'next': openapi.Schema(type=openapi.TYPE_ARRAY, description='Children Objects', items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'next': openapi.Schema(type=openapi.TYPE_STRING, description='Children of Child Object (無限に続くので String にしてある)')})),
    }),
    responses={200: 'OK', 400: 'Bad Request'})
@api_view(['GET'])
def fork_tree(request, id_repository):
  print(id_repository)

  mRepo = fetch_repo(id_repository)  

  while mRepo.id_fork_from:
    mRepo = fetch_repo(str(mRepo.id_fork_from))

  tree = mk_tree(mRepo)

  return Response(tree, status=status.HTTP_200_OK)