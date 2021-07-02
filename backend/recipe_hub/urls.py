from django.urls import path, include
from . import views

urlpatterns = [
  path(r'fork', views.fork),
  path(r'fork-tree/<str:id_repository>', views.fork_tree),
  path(r'mrepository/<str:id_repository>', views.repo),
  path(r'mrepository', views.repo_select),
  path(r'mimage/<str:id_author>', views.image_select)
]
