from django.db import models
from .managers import ThreadManager

# Create your models here.


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Thread(TrackingModel):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group'),
    )

    name = models.CharField(max_length=50, blank=True, null=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
    users = models.ManyToManyField('auth.User')
    objects = ThreadManager()

    def __str__(self) -> str:

        if self.thread_type == 'personal' and self.users.count() == 2:
            return '{0} and {1}'.format(self.users.first(), self.users.last()) 
        return self.name


class Message(TrackingModel):
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self) -> str:
        return 'From <{0}>'.format(self.thread)


"""
class Message(TrackingModel):
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return 'From <{0}>'.format(self.thread)
"""