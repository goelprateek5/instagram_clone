from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
import uuid
from notifications.models import notification

def user_directory_path(instance, filename):
    # this file will be uploaded to MEDIA_ROOT /user_(id)/filename
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class PostFileContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
    file = models.FileField(upload_to=user_directory_path)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.ManyToManyField(PostFileContent, related_name='content')
    caption = models.TextField(max_length=1500, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('postdetails', args=[str(self.id)])

    def __str__(self):
        return str(self.id)

    def update_like(sender, instance, *args, **kwargs):
        post = instance.post
        likes = Likes.objects.filter(post = post).count()
        post.likes = likes
        post.save()

    
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def follow_notification(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

        notify = notification(sender=sender, user = following, notification_type=3)
        notify.save()
        

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            stream = Stream(post = post, user = follower.follower, date = post.posted, following = user)
            stream.save()

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def like_notification(sender, instance, *args, **kwargs):
        liked = instance
        post = liked.post
        sender = liked.user
        notify = notification(post = post, sender=sender, user=post.user, notification_type=1)
        notify.save()
    
    def unlike_notification(sender, instance, *args, **kwargs):
        liked = instance
        post = liked.post
        sender = liked.user
        notify = notification.objects.filter(post = post, sender=sender, user=post.user, notification_type=1)
        notify.delete()


post_save.connect(Stream.add_post, sender = Post)

#Likes
post_save.connect(Post.update_like, sender = Likes)
post_delete.connect(Post.update_like, sender = Likes)
post_save.connect(Likes.like_notification, sender = Likes)
post_delete.connect(Likes.unlike_notification, sender = Likes)

#follow
post_save.connect(Follow.follow_notification, sender = Follow)