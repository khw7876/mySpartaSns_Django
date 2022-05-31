import django
from django.shortcuts import render, redirect
from requests import RequestException

from user.models import UserModel
from .models import TweetComment, TweetModel
from django.contrib.auth.decorators import login_required 


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else :
        return redirect('/sign-in')


@login_required 
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request,'tweet/tweet_detail.html',{'tweet':my_tweet,'comment':tweet_comment})

def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated

        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at') #모든 모델을 불러오는데, 생성순서 역순대로 불어와라

            return render(request, 'tweet/home.html',{'tweet': all_tweet})
        else:
            return redirect('/sign-in')


@login_required #위에서 import했는데, 로그인이 되어 있어야만 접근이 가능하다.
def delete_tweet(request,id):
    my_tweet = TweetModel.objects.get(id=id) #Tweet 모델에서 id가 request의 id인것을 가져온다.
    my_tweet.delete()
    return redirect('/tweet')

    
@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment","")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/'+str(id))


@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))