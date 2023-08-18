from django.urls import path
from .views import TakePhotoView

urlpatterns = [
    path('register/', TakePhotoView.as_view(), name='register'),

]
