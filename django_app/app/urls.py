from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('review_evaluation', views.review_evaluation, name='review_evaluation'),
]