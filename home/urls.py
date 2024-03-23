from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name='home'),
    path("image-adding/", views.image_adding, name="home-image-adding"),
    path("image-annotation/", views.image_annotation, name="home-image-annotation"),
    path("image-removing/", views.image_removing, name='home-image-removing')
]