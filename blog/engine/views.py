from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from engine.models import Post, Comment, CommentForm, Tag
from django.forms.models import ModelForm
from datetime import datetime

def index(request):
    posts = Post.objects.all()[:10]
    is_user_auth = request.user.is_authenticated()
    return render_to_response('index.html', { "posts": posts, 
                                              "is_user_auth": is_user_auth })

def post_by_date_and_slug(request, year, month, day, slug):
    date = "-".join([str(year).zfill(4), str(month).zfill(2), str(day).zfill(2)])
    try:
        post = Post.objects.get_by_date_and_slug(date, slug)
    except Post.DoesNotExist:
        raise Http404
    return render_post(request, post)
    
def posts_by_tag(request, tag):
    tag = get_object_or_404(Tag, text=tag)
    posts = tag.post_set.all()
    is_user_auth = request.user.is_authenticated()
    return render_to_response('index.html', { "posts": posts, 
                                              "is_user_auth": is_user_auth })

def post_by_id(request, number, form = CommentForm()):
    post = get_object_or_404(Post, pk=int(number))
    return render_post(request, post, form)

def render_post(request, post, form = CommentForm()):
    comments = post.comment_set.all()
    comments_count = comments.count()
    has_comments = comments_count > 0
    is_user_auth = request.user.is_authenticated()
    author = ""
    email = ""
    website = ""
    if request.user.is_authenticated():
        author = request.user.username
        email = request.user.email
        website = "http://localhost:8000/"
    return render_to_response('post.html', { "post": post, 
                                             "comments": comments,
                                             "comments_count": comments_count,
                                             "has_comments": has_comments,
                                             "form": form,
                                             "author": author,
                                             "email": email,
                                             "website": website,
                                             "is_user_auth": is_user_auth })

def add_comment(request, number):
    form = CommentForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/" + Post.objects.get(id=int(number)).get_nice_url())

    return post_by_id(request, number, form)
