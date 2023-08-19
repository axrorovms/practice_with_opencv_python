import os
import time
import cv2
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from .models import User
from .serializer import UserSerializer


class TakePhotoView(CreateAPIView):
    serializer_class = UserSerializer

    def video_to_image_and_save_db(self, video_path, username):
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()

        if ret:
            if not os.path.exists('media/user_photos'):
                os.makedirs('media/user_photos')
                if not os.path.exists('media/user_videos'):
                    os.makedirs('media/user_videos')
            video_db_path = os.path.join('media', 'user_videos', f'{username}.avi')
            image_path = os.path.join('media', 'user_photos', f'{username}.jpg')
            cv2.imwrite(image_path, frame)
            out = cv2.VideoWriter(video_db_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))

            while ret:
                out.write(frame)  # Write each frame to the video
                ret, frame = cap.read()

            out.release()
            cap.release()

            User.objects.create(username=username, face_image=image_path, face_video=video_db_path)

        else:
            cap.release()

    def create(self, request, *args, **kwargs):
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('temp_video.avi', fourcc, 20.0, (640, 480))

        start_time = time.time()
        recording_time = 3

        while True:
            ret, frame = cap.read()

            if ret:
                out.write(frame)
                cv2.imshow('Video', frame)

                if time.time() - start_time >= recording_time:
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        self.video_to_image_and_save_db('temp_video.avi', request.data.get('username'))

        return Response({'message': 'Video recorded and converted to image'}, status=status.HTTP_201_CREATED)
