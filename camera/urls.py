from django.urls import path
from .views import TakePhotoView

urlpatterns = [
    path('register/', TakePhotoView.as_view(), name='register'),

]

#
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('take_photo/', views.take_photo_view, name='take_photo'),
# ]
