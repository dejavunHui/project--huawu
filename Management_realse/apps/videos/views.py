from django.shortcuts import render,redirect
from django.views.generic import View,CreateView
from django.urls import reverse

from ..videos.models import Videos,Upload
from .forms import UploadFileForm
from .tasks import VideoSRTask
# Create your views here.



class VideoListView(View):

    def typeDict(self,page_id):
        type_dict = {
            1:'kongbu',
            2:'aiqing',
            3:'xiju',
            4:'juqing',
            5:'kehuan',
            6:'zhanzheng',
            7:'jilu',
            8:'dongzuo'
        }
        return type_dict.get(page_id)
    '''视频管理页面'''
    def get(self,request,*args,**kwargs):

        # users = Admain.objects.all()
        type = kwargs.get('type')
        if request.user.is_authenticated:
            if not type:
                videos = Videos.objects.filter(type = self.typeDict(1))
                return render(request,'video/kongbu.html',{'videos':videos,'name':request.user.username})
            else:
                videos = Videos.objects.filter(type = self.typeDict(type))
                return render(request,'video/'+self.typeDict(type)+'.html',{'videos':videos,'name':request.user.username})

        else:

            url = reverse('login:index')
            response = redirect(url)
            return response


class UploadFileView(View):

    def get(self,request):
        obj = UploadFileForm()
        return render(request,'video/upload.html',{'obj':obj})

    def post(self,request,*args,**kwargs):
        '''上传文件'''
        base_url = 'http://60.205.221.200:80/'
        obj = UploadFileForm(request.POST,request.FILES)
        if obj.is_valid():
            #验证成功
            upload = Upload(img=request.FILES.get('img'),sr_video=request.FILES.get('src_video'))
            # print(request.FILES.get('img'))
            upload.save()
            #上传数据成功
            kv = {}
            kv['type'] = obj.cleaned_data.get('type')
            kv['name'] = obj.cleaned_data.get('name')
            kv['year'] = obj.cleaned_data.get('year')
            kv['info'] = obj.cleaned_data.get('info')
            kv['img'] = base_url + obj.cleaned_data.get('img').name
            video_name = obj.cleaned_data.get('src_video').name
            kv['sr_video'] = base_url + 'src_video/' + video_name
            kv['x2_video'] = base_url +  'x2video/' + video_name
            kv['x3_video'] = base_url +  'x3video/' + video_name
            kv['x4_video'] = base_url + 'x4video/' + video_name

            try:
                VideoSRTask.apply_async(kwargs = {'name':video_name.split('.')[0]})
                kv['flag'] = 1
            except:
                kv['flag'] = 0

            video = Videos(**kv)
            video.save()

            # print(obj.cleaned_data.get('src_video').name)
            return render(request,'video/upload.html',{'obj':UploadFileForm(),'message':obj.cleaned_data.get('name') + '上传成功'})
        else:
            return render(request, 'video/upload.html', {'obj': UploadFileForm(),'message':obj.name + '上传失败'})

class VideoInfoView(View):

    def get(self,request,*args,**kwargs):

        video_id = kwargs.get('video_id')
        video = Videos.objects.get(id = video_id)

        return render(request,'video/content.html',{'video':video,'name':request.user.username})

    def post(self,request,*args,**kwargs):

        # print(request.body,request.POST)
        id = request.POST.get('id')

        kv = {}
        kv['name'] = request.POST.get('name')
        kv['year'] = request.POST.get('year')
        kv['type'] = request.POST.get('type')
        kv['info'] = request.POST.get('info')

        if request.POST.get('op') == 'change':
            Videos.objects.filter(id = id).update(**kv)
            return render(request,'video/content.html',{'video':Videos.objects.get(id = id),'name':request.user.username,'message':'影片更新成功'})

        elif request.POST.get('op') == 'delete':
            try:
                Videos.objects.get(id = id).delete()
            except:
                pass
            video = Videos.objects.get(id = str(int(id) + 1))
            if not video:
                video = Videos.objects.get(id=str(int(id) - 1))

            return render(request, 'video/content.html',
                          {'video': video, 'name': request.user.username, 'message':kv.get('name') + '删除成功'})
        else:
            return render(request,'video/content.html',{'video':Videos.objects.get(id = id),'name':request.user.username})