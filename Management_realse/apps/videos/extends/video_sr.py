from .build import build_model,generate_image
import os
# from ..Management_realse import video_sr_config as config
import cv2
import subprocess

'''
视频超清化
'''

class VideoSROptions(object):

    def __init__(self,config):
        self.config = config

        self.model_dict = {
            2:build_model(config.CHECKPOINT_DIR,2),
            3:build_model(config.CHECKPOINT_DIR,3),
            4:build_model(config.CHECKPOINT_DIR,4)
        }


    def gen(self,src_video_dir,SR_video_dir,output,video_name):
        '''

        :param src_video_dir: 源视频路径
        :param SR_video_dir: 超分视频路径
        :param output: 合并结果文件路径
        :param video_name: 视频名称

        :return:
        '''
        audio_path = self.config.AUDIO_PATH#音频临时存放
        src_video = os.path.join(src_video_dir,video_name+'.mp4')#源视频
        sr_video_temp = self.config.MERVO_PATH#合并视频临时存放
        
		
        if not os.path.exists(audio_path):
            os.makedirs(audio_path)

        if not os.path.exists(sr_video_temp):
            os.makedirs(sr_video_temp)
        
        #合并结果路径生成
        if not os.path.exists(os.path.splitext(output)[0]):
            os.makedirs(os.path.splitext(output)[0])


        if os.path.splitext(src_video)[1] != '.mp4':
            
            return
        acc_path = os.path.join(audio_path,video_name+'.mp3')
        if not os.path.exists(acc_path):
            acc = 'ffmpeg -i '+src_video + ' -f mp3 -vn ' + acc_path#提取音频
            a = subprocess.call(acc,shell=True)
       
		
        sr_video_unzip = os.path.join(sr_video_temp,video_name+'.mp4')#未压缩超分视频临时文件路径
        #sr_video_zip = os.path.join(SR_video_dir,video_name+'.mp4').replace('\\','/')
       
        #合并视频
        combine = 'ffmpeg -i ' + SR_video_dir + ' -i ' + acc_path + ' ' + sr_video_unzip
        a = subprocess.call(combine,shell=True)
        
        
        #压缩视频
        zips = 'ffmpeg -i ' + sr_video_unzip + ' -b:v 500k ' + output
        _ = subprocess.call(zips,shell = True)





    def SR(self,video_name = None):

        if not video_name:
            return
		#print('start..')
        video = os.path.join(self.config.SRC,video_name+'.mp4').replace('\\','/')
        # x2out = os.path.join(config.VIDEO_DIC.get(2),video_name)
        # x3out = os.path.join(config.VIDEO_DIC.get(3), video_name)
        # x4out = os.path.join(config.VIDEO_DIC.get(4), video_name)
		#结果视频存放路径
        out_dic = {
            2:os.path.join(self.config.VIDEO_DIC.get(2),video_name+'.mp4'),
            3:os.path.join(self.config.VIDEO_DIC.get(3), video_name+'.mp4'),
            4:os.path.join(self.config.VIDEO_DIC.get(4), video_name+'.mp4')
        }
        if not os.path.exists(self.config.VODEO_PATH):
            os.makedirs(self.config.VODEO_PATH)


        if not os.path.isfile(video):
            # print('start')
            return

        else:
            #一种倍数提升多次


            videoCapture = cv2.VideoCapture(video)
            fps = videoCapture.get(cv2.CAP_PROP_FPS)
            UPSCALE_FACTOR = self.config.UPSCALE_FACTOR
            size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH) * UPSCALE_FACTOR),
                    int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)) * UPSCALE_FACTOR)
            output_name = self.config.VODEO_PATH+video_name+'.avi'

            videoWriter = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*'MJPG'), fps, size)
            success, frame = videoCapture.read()
            while success:
               out_img = generate_image(self.model_dict.get(UPSCALE_FACTOR), frame)
               videoWriter.write(out_img)
               success, frame = videoCapture.read()
            self.gen(self.config.SRC,output_name,out_dic.get(UPSCALE_FACTOR),video_name)
            # print('succed %s'%UPSCALE_FACTOR)
				
            #多种倍数提升一次
#            videoCapture = cv2.VideoCapture(video)
#            fps = videoCapture.get(cv2.CAP_PROP_FPS)
#            for UPSCALE_FACTOR in range(2,5):
#                size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH) * UPSCALE_FACTOR),
#							int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)) * UPSCALE_FACTOR)
#                output_name = self.config.VODEO_PATH+video_name+'_'+str(i+1)+'.avi'
#                if not os.path.exists(self.config.VODEO_PATH+video_name):
#                    os.makedirs(self.config.VODEO_PATH+video_name)
#                videoWriter = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*'MJPG'), fps, size)
#                success, frame = videoCapture.read()
#            while success:
#               out_img = generate_image(self.model_dict.get(UPSCALE_FACTOR), frame)
#               videoWriter.write(out_img)
#               success, frame = videoCapture.read()
#					
#            self.gen(self.config.SRC,output_name,out_dic.get(UPSCALE_FACTOR),video_name)
#            print('succed %s'%UPSCALE_FACTOR)


if __name__ == '__main__':
    import video_sr_config
    vv = VideoSROptions(video_sr_config)
    vv.SR('陈伟霆献唱《橙红年代》主题曲《光》_标清')