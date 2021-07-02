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

@transaction.atomic
@swagger_auto_schema(methods=['get'],
    responses={200: 'OK', 400: 'Bad Request'})
@api_view(['GET'])
def image_select(request, id_author):
  mImageList = MImage.objects.filter(id_author=id_author)

  return Response(MImageSerializer(mImageList, many=True).data, status.HTTP_200_OK)