from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
import cv2
import os


class TakePhotoView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()

        if ret:
            if not os.path.exists('media/user_photos'):
                os.mkdir('media/user_photos')
            photo_path = os.path.join('media', 'user_photos', f'{username}.jpg')
            cv2.imwrite(photo_path, frame)

            User.objects.create(username=username, face_image=photo_path)

            cap.release()
            return Response({'message': 'Photo taken and uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            cap.release()
            return Response({'message': 'Failed to capture photo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)