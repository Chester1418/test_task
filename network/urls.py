from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, base_name="posts")


urlpatterns = [
    path('signup/', signup)
]+router.urls