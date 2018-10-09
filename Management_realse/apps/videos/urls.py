from django.urls import path
from . import views

app_name = 'videos'
urlpatterns = [
    path('index/',views.VideoListView.as_view(),name = 'index'),
    path('<int:type>/',views.VideoListView.as_view(),name = 'types'),
    path('upload/',views.UploadFileView.as_view(),name = 'upload'),
    path('info/<int:video_id>',views.VideoInfoView.as_view(),name = 'info')
]