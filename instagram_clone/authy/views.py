from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User
from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, login

from .models import Profile
from post.models import Post, Follow, Stream
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator
from django.urls import resolve, reverse

# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name

	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')
	elif(url_name == 'profilefavorite' and str(username)!=str(request.user)):
		return HttpResponseRedirect(reverse('profile', args=[username]))
	else:
		posts = profile.favorites.all()

	#profile info stats
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	follower_count = Follow.objects.filter(following=user).count()
	
	#follow button status checks
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#Pagination
	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': posts_paginator,
		'profile':profile,
		'url_name':url_name,
		'posts_count':posts_count,
		'following_count':following_count,
		'follower_count':follower_count,
		'follow_status': follow_status,
	}

	return HttpResponse(template.render(context, request))


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			user = User.objects.create_user(username=username, email=email, password=password, last_name=last_name, first_name=first_name)
			user.save()
			profile = Profile.objects.get(user=user)
			profile.first_name = first_name
			profile.last_name = last_name
			profile.save()
			new_user = authenticate(username=form.cleaned_data.get('username'), password = form.cleaned_data.get('password'))
			login(request, new_user)
			return HttpResponseRedirect(reverse('edit_profile'))
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return HttpResponseRedirect(reverse('profile', args=[request.user]))
	else:
		form = EditProfileForm()

	context = {
		'form':form,
	}

	return render(request, 'edit_profile.html', context)

@login_required
def follow(request, username, option):
	user = request.user
	following = get_object_or_404(User, username = username)

	try:
		f, created = Follow.objects.get_or_create(follower = user, following=following)

		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=user).all().delete()
		else:
			posts = Post.objects.all().filter(user=following)[:10]

			with transaction.atomic():
				for post in posts:
					stream = Stream(post=post, user=user, date=post.posted, following=following)
					stream.save()
		return HttpResponseRedirect(reverse('profile', args=[username]))
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))