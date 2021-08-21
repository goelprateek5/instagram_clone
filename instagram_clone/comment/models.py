from django.db import models
from post.models import Post
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from notifications.models import notification

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def comment_notification(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.body[:90]
        sender = comment.user
        notify = notification(post = post, sender=sender, user=post.user, notification_type=2, text_preview=text_preview)
        notify.save()

    def delete_comment_notification(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.post

        notify = notification.objects.filter(post=post, sender=sender, notification_type=2, user=post.user)
        notify.delete()

post_save.connect(Comment.comment_notification, sender = Comment)
post_delete.connect(Comment.delete_comment_notification, sender = Comment)