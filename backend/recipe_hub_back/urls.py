"""recipe_hub_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers
from recipe_hub import views

schema_view = get_swagger_view(title='API Lists')

router = routers.DefaultRouter()
router.register('muser', views.MUserViewSet, basename='MUser')
router.register('mrepository', views.MRepositoryViewSet, basename='MRepository')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/v1/', include(router.urls)),
    path('api/v1/', include("recipe_hub.urls")),
    path('swagger/', schema_view)
]
