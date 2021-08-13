from typing import List
from django import template
from django.shortcuts import render, redirect, get_object_or_404
from django.template import context, loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from post.models import Post, Stream, Tag, Likes
from post.forms import NewPostForm
from authy.models import Profile
from comment.models import Comment
from comment.forms import CommentForm

@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    liked_posts = []
    #like button logic
    likes = Likes.objects.filter(user=user)
    for like in likes:
        liked_posts.append(like.post.id)
    # print(liked_posts)

    groups_ids = []

    for post in posts:
        groups_ids.append(post.post_id)

    post_items = Post.objects.filter(id__in=groups_ids).all().order_by('-posted')
    # print(type(post_items[0].id))

    template = loader.get_template('index.html')
    context = {
        'post_items': post_items,
        'liked_posts':liked_posts
    }

    return HttpResponse(template.render(context, request))

@login_required
def PostDetails(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    favorited = False
    liked = False

    comments = Comment.objects.filter(post=post).order_by('date')

    #comment form
    if request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('postdetails', args = [post_id]))
    else:
        form = CommentForm()
    
    #favorite check
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=user)

        if profile.favorites.filter(id=post_id).exists():
            favorited = True

    #liked check
    if request.user.is_authenticated:
        if Likes.objects.filter(user=user, post=post).exists():
            liked = True

    template = loader.get_template('post_detail.html')

    context = {
        'post':post,
        'favorited':favorited,
        'comments':comments,
        'form':form,
        'liked': liked
    }

    return HttpResponse(template.render(context,request))

@login_required
def NewPost(request):
    user = request.user.id
    tags_obs = []

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag.strip())
                tags_obs.append(t)
            
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_obs)
            p.save()

            return redirect('index')

    else:
        form = NewPostForm()

    context = {
        'form': form,
    }

    return render(request, 'newpost.html', context)

@login_required
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    template = loader.get_template('tag.html')

    context = {
        'posts':posts,
        'tag':tag,
    }

    return HttpResponse(template.render(context,request))

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    current_likes = post.likes

    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user,post=post)
    else:
        Likes.objects.filter(user=user, post=post).delete()    

    return HttpResponseRedirect(reverse('postdetails', args = [post_id]))

@login_required
def favorite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    profile = Profile.objects.get(user=user)

    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)

    return HttpResponseRedirect(reverse('postdetails', args = [post_id]))

