# tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('tweet/', views.tweet, name='tweet'), # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('tweet/delete/<int:id>', views.delete_tweet, name='delete-tweet'), #<int:id>는 해당 id값이 int로 들어간다. (주소에 id가 들어가는 형식)
    path('tweet/<int:id>',views.detail_tweet,name='detail-tweet'), # 댓글을 보기 위해서 상세 페이지로 이동하는 detail_tweet 함수
    path('tweet/comment/<int:id>',views.write_comment, name='write-comment'), # 댓글을 작성하는 write_comment
    path('tweet/comment/delete/<int:id>',views.delete_comment, name='delete-comment'),
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
]