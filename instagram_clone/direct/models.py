from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.core.validators import MinLengthValidator



# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recepient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000, validators=[MinLengthValidator(1)])
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return "User: "+str(self.user.username)+" sender: "+str(self.sender.username)+" recepient: "+str(self.recepient.username)+" body: "+str(self.body)

    def send_message(from_user, to_user, body):
        sender_message = Message(
            user= from_user,
            sender = from_user,
            recepient = to_user,
            body = body,
            is_read=True,
        )
        sender_message.save()

        recepient_message = Message(
            user= to_user,
            sender = from_user,
            recepient = from_user,
            body = body,
        )
        recepient_message.save()

        return sender_message

    def get_messages(user):
        users = []
        messages = Message.objects.filter(user=user).values('recepient').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recepient']),
                'last': message['last'],
                'unread':Message.objects.filter(user = user, recepient=message['recepient'], is_read=False).count()
            })

        return users