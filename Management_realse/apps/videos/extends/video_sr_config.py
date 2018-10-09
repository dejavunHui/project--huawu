
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CHECKPOINT_DIR = './checkpoint'

VIDEO_DIC = {
    1:'/home/hui/video',
    2:'/home/hui/video/videox2',
    3:'/home/hui/video//videox3',
    4:'/home/hui/video//videox4',

}
#放大倍数
UPSCALE_FACTOR = 2

#临时音频存储
AUDIO_PATH = './video/audio_temp'
#临时存储放大视频
VODEO_PATH = './video/video_temp'
#临时存储合并视频
MERVO_PATH = './video/mervi_temp'

SRC = '/home/hui/video/src_video'
# X2VIDEO = '/home/hui/video/x2video'
# X3VIDEO = '/home/hui/video/x3video'
# X4VIDEO = '/home/hui/video/x4video'
