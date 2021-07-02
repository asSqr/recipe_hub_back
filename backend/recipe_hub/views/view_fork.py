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

  id_user = data.get('id_user')
  author_name = data.get('author_name')
  author_photo_url = data.get('author_photo_url')
  id_repo = data.get('id_repo')
  name = data.get('name')
  title = data.get('title')
  recipe = data.get('recipe')
  genre = data.get('genre')
  thumbnail = data.get('thumbnail')

  mRepo = MRepository.objects.filter(id=id_repo)

  if len(mRepo) != 1:
    raise ValueError('Illegal Argument: id_repo is not unique {}'.format(id_repo))

  mRepo = mRepo[0]

  mRepoObj = {}
  mRepoObj['id_author'] = id_user if id_user is not None else mRepo.id_author
  mRepoObj['author_photo_url'] = author_photo_url if author_photo_url is not None else mRepo.author_photo_url
  mRepoObj['author_name'] = author_name if author_name is not None else mRepo.author_name
  mRepoObj['id_fork_from'] = id_repo
  mRepoObj['name'] = name if name is not None else mRepo.name
  mRepoObj['title'] = title if title is not None else mRepo.title
  mRepoObj['recipe'] = recipe if recipe is not None else mRepo.recipe
  mRepoObj['genre'] = genre if genre is not None else mRepo.genre
  mRepoObj['is_temp'] = True

  if thumbnail or mRepo.thumbnail:
    mRepoObj['thumbnail'] = thumbnail if thumbnail is not None else mRepo.thumbnail 

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

  return Response({'id': str(newMRepo.id)}, status=status.HTTP_201_CREATED)

def fetch_repo(id_repo):
  mRepo = MRepository.objects.filter(id=id_repo)

  if len(mRepo) != 1:
    raise ValueError('Illegal Argument: id_repo is not unique {}'.format(id_repo))

  return mRepo[0]

def patch_repo(mRepo, param):
  mRepoObj = {}
  mRepoObj['id_author'] = param.get('id_author') if param.get('id_author') is not None else mRepo.id_author
  mRepoObj['author_photo_url'] = param.get('author_photo_url') if param.get('author_photo_url') is not None else mRepo.author_photo_url
  mRepoObj['author_name'] = param.get('author_name') if param.get('author_name') is not None else mRepo.author_name
  mRepoObj['id_fork_from'] = param.get('id_fork_from', '$') if param.get('id_fork_from', '$') != '$' else mRepo.id_fork_from
  mRepoObj['id_fork_to_list'] = param.get('id_fork_to_list') if param.get('id_fork_to_list') is not None else mRepo.id_fork_to_list
  mRepoObj['name'] = param.get('name') if param.get('name') is not None else mRepo.name
  mRepoObj['title'] = param.get('title') if param.get('title') is not None else mRepo.title
  mRepoObj['recipe'] = param.get('recipe') if param.get('recipe') is not None else mRepo.recipe
  mRepoObj['genre'] = param.get('genre') if param.get('genre') is not None else mRepo.genre

  if param.get('thumbnail') or mRepo.thumbnail:
    mRepoObj['thumbnail'] = param.get('thumbnail') if param.get('thumbnail') is not None else mRepo.thumbnail 

  mRepoSerializer = MRepositorySerializer(mRepo, data=mRepoObj, partial=True)

  if mRepoSerializer.is_valid(raise_exception=True):
    print(mRepoSerializer.errors)
    mRepoSerializer.save()
  else:
    return Response(mRepoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


def mk_tree(mRepo):
  fork_list = json.loads(mRepo.id_fork_to_list)

  ret = {}

  children = []

  if 'list' in fork_list:
    for id_repo in fork_list['list']:
      children.append(mk_tree(fetch_repo(id_repo)))

  ret['id'] = str(mRepo.id)
  ret['title'] = mRepo.title
  ret['name'] = mRepo.name
  ret['recipe'] = mRepo.recipe
  ret['genre'] = mRepo.genre
  ret['id_author'] = mRepo.id_author
  if mRepo.author_name:
    ret['author_name'] = mRepo.author_name
  if mRepo.author_photo_url:
    ret['author_photo_url'] = mRepo.author_photo_url
  if mRepo.thumbnail:
    ret['thumbnail'] = str(mRepo.thumbnail.url)
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

def setForkFrom(id_repo, id_fork_from):
  mRepo = fetch_repo(id_repo)

  patch_repo(mRepo, {
    'id_fork_from': id_fork_from
  })

def deleteForkFrom(id_repo):
  mRepo = fetch_repo(id_repo)

  patch_repo(mRepo, {
    'id_fork_from': None
  })

@transaction.atomic
@swagger_auto_schema(methods=['delete'], responses={201: 'Created', 400: 'Bad Request'})
@api_view(['DELETE'])
def repo(request, id_repository):
  print(id_repository)

  mRepo = fetch_repo(id_repository)  

  fork_list = json.loads(mRepo.id_fork_to_list)

  if mRepo.id_fork_from and 'list' in fork_list:
    for id_repo in fork_list['list']:
      setForkFrom(id_repo, mRepo.id_fork_from)
  elif 'list' in fork_list:
    for id_repo in fork_list['list']:
      deleteForkFrom(id_repo)

  if mRepo.id_fork_from:
    mParent = fetch_repo(str(mRepo.id_fork_from))

    parent_fork_list = json.loads(mParent.id_fork_to_list)

    if 'list' in fork_list:
      for id_repo in fork_list['list']: 
        parent_fork_list['list'].append(id_repo)   

    parent_fork_list['list'].remove(str(mRepo.id))

    patch_repo(mParent, {
      'id_fork_to_list': json.dumps(parent_fork_list)
    })

  mRepo.delete()

  return Response({}, status=status.HTTP_200_OK)

@transaction.atomic
@swagger_auto_schema(methods=['get'],
    responses={200: 'OK', 400: 'Bad Request'})
@api_view(['GET'])
def repo_select(request):
  mRepoList = MRepository.objects.filter(is_temp=False)

  return Response(MRepositorySerializer(mRepoList, many=True).data, status.HTTP_200_OK)