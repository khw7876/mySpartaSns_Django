import django
from django.shortcuts import render, redirect
from mysqlx import Auth
from requests import RequestException
from django.views.generic import ListView, TemplateView
from user.models import UserModel
from .models import TweetComment, TweetModel
from django.contrib.auth.decorators import login_required #로그인이 되어 있어야만 실행시키는 얘

# Create your views here.

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else :
        return redirect('/sign-in')

#상세 페이지를 불러주는 함수
@login_required
def detail_tweet(request, id):
    if request.method == "GET":
        my_tweet = TweetModel.objects.get(id=id)
        my_comment = TweetComment.objects.filter(tweet_id = id).order_by('-created_at')
        return render(request, 'tweet/tweet_detail.html', {'tweet' : my_tweet, 'comment':my_comment})


def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated

        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at') #모든 모델을 불러오는데, 생성순서 역순대로 불어와라

            return render(request, 'tweet/home.html',{'tweet': all_tweet})
        else:
            return redirect('/sign-in')

    elif request.method =='POST':
        user = request.user  #로그인이 되어있는 유저의 전체 정보를 가져옴
        content = request.POST.get('my-content','')
        tags = request.POST.get('tag', '').split(',')
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at') #모든 모델을 불러오는데, 생성순서 역순대로 불어와라
            return render(request,'tweet/home.html', {'error' : '글은 공백일 수 없습니다.', 'tweet' : all_tweet})
        
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '': # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')





# 홈 화면에서 tweet를 삭제하는 함수
@login_required #위에서 import했는데, 로그인이 되어 있어야만 접근이 가능하다.
def delete_tweet(request,id):
    my_tweet = TweetModel.objects.get(id=id) #Tweet 모델에서 id가 request의 id인것을 가져온다.
    my_tweet.delete()
    return redirect('/tweet')




# 상세 페이지에서 댓글을 쓰는 함수
@login_required 
def write_comment(request,id):
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        tweet_id = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.tweet = tweet_id  # 모델에서 보면 외래키를 가져오라함.
        # 궁금한 점 1 : 왜 얘는 아이디만 가져오는가
        TC.author = request.user   # request안에 이미 user가 있음.
        # 궁금한 점 2 : 왜 얘는 model에서 가져오는게 아닌가.
        # ex) UserModel.objects.get(id=id) 해도 똑같은 건가?
        TC.comment = comment
        TC.save()
        
        return redirect('/tweet/'+str(id))

# 상세 페이지에서 댓글을 삭제하는 함수
@login_required
def delete_comment(request, id):
    tweet_id = TweetComment.objects.get(id=id)
    tweet_id.delete()
    return redirect('/tweet/'+str(tweet_id))



class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

