from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import login,authenticate
from . import models
from hashlib import md5
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class LoginView(View):

    '''
    管理员登录
    '''

    def __myhash__(self,info):
        hash = md5()
        hash.update(bytes(str(info), encoding='utf-8'))
        return hash.hexdigest()

    def get(self,request):
        '''
        显示
        :param request:
        :return:
        '''
        return render(request,'login/index.html')

    def post(self,request):

        '''登录验证'''
        username = request.POST.get('value_1')
        password = request.POST.get('value_2')

        if not all([username,password]):
            return render(request,'login/index.html',{'message':'信息填写不完整'})
        password = self.__myhash__(password)
        try:
            admain = models.Admain.objects.get(username=username,password=password)
            # admain = authenticate(username = username,password = password)
            if admain and admain.is_active:
                # 用户激活
                login(request,admain)


                # 用户登录默认跳转
                next_url = request.GET.get('next', reverse('videos:index'))

                response = redirect(next_url)

                response.delete_cookie('value_1')
                # response.set_cookie('value_1', username, max_age=7 * 24 * 3600)
                return response
            else:
                return render(request, 'login/index.html', {'message': '用户未激活'})
        except:
            return render(request,'login/index.html',{'message':'用户名或者密码错误'})

