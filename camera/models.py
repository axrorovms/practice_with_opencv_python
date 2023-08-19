from django.db import models
from django.core.validators import RegexValidator, ValidationError
import datetime
import uuid

MEDIA_TYPES = {
    r'^(jpg|jpeg|png|JPG)$': 'media',
    r'^(mp4)$': 'videos'
}

FILE_TYPES = {
    r'^(jpg|jpeg|png|JPG)$': 'images',
    r'^(pdf)$': 'documents',
    r'^(mp4)$': 'videos'
}


def upload_name(instance, filename):
    file_type = filename.split('.')[-1]
    date = datetime.datetime.now().strftime('%Y/%m/%d')

    for regex, folder in FILE_TYPES.items():
        try:
            RegexValidator(regex).__call__(file_type)
            return '%s/%s/%s/%s.%s' % (folder, instance._meta.model_name, date, uuid.uuid4(), file_type)
        except ValidationError:
            pass
    raise ValidationError('File type is unacceptable')


class User(models.Model):
    username = models.CharField(max_length=100)
    face_image = models.ImageField(upload_to=upload_name)
    face_video = models.FileField(upload_to=upload_name)