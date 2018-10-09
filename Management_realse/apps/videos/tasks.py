
from celery.task import Task
from .extends.video_sr import VideoSROptions
from .extends import video_sr_config

class VideoSRTask(Task):


    def run(self, *args, **kwargs):

        video_name = kwargs.get('name')

        vv = VideoSROptions(video_sr_config)
        vv.SR(video_name)
