from django.db import models
import os
from django.conf import settings

# Create your models here.
class Videos(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=20,unique=True)
    year = models.IntegerField(verbose_name='年份')
    info = models.TextField()
    img = models.URLField(null=True)
    sr_video = models.URLField()
    x2_video = models.URLField(null = True)
    x3_video = models.URLField(null=True)
    x4_video = models.URLField(null=True)
    flag = models.IntegerField(default=0)

    class Meta:
        db_table = 'app_videos'
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name


__VIDEO_PATH = os.path.join(settings.BASE_DIR,'video')
__IMG_PATH = os.path.join(settings.BASE_DIR,'img')


def img_dir(instance,filename):
    return os.path.join(__IMG_PATH,filename)

def src_video_dir(instance,filename):
    return os.path.join(__VIDEO_PATH,'video_src',filename)



class Upload(models.Model):
    img = models.ImageField(verbose_name='图片上传路径',upload_to=img_dir)
    sr_video = models.FileField(verbose_name='源视频上传路径',upload_to=src_video_dir)
    class Meta:
        db_table = 'app_uploads'
        verbose_name = '上传存储路径'
        verbose_name_plural = verbose_name

# 1 | 439b6cdd39232649aaf80fdef215dccb | 2018-10-03 13:21:34.944062 | 17636631772 |         1 |