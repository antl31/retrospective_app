from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

MEETINGS = [('standard', 'STANDARD'), ('other_type', 'OTHER_TYPE')]
STATUS = [('DONE', 'done'), ('IN PROGRESS', 'in progress')]
PRIORITY = [('HIGH', 'high'), ("MIDDLE", "middle"), ('LOW', 'low')]
CARD_TYPE = [('simple_card', 'SIMPLE'), ('action_item', 'ACTION_ITEM')]


class Teams(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)
    members = ArrayField(models.IntegerField(null=True, blank=False), null=True, blank=True, default=list)
    tags = ArrayField(models.CharField(max_length=50), default=list, null=True, blank=True)

    def __str__(self):
        return self.name


class Retros(models.Model):
    name = models.CharField(max_length=30, null=False, blank=True, unique=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    meeting_format = models.CharField(max_length=25, choices=MEETINGS, default='standard', null=True, blank=True)
    fk_team = models.ForeignKey('Teams', on_delete=models.CASCADE)

    def __str__(self):
        return f'name: {self.name} team:{self.fk_team}'


class Cards(models.Model):
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=30, null=True, blank=True, choices=CARD_TYPE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_anonymus = models.NullBooleanField(null=True, blank=True)
    retro_fk = models.ForeignKey('Retros', on_delete=models.CASCADE)
    tags = ArrayField(models.CharField(max_length=30), default=list, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS, null=True, blank=True)
    priority = models.CharField(max_length=30, choices=PRIORITY, null=True, blank=True)
    asignee = ArrayField(models.CharField(max_length=50, null=True, blank=False), blank=True, default=list)
    likes = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'description: {self.description[1:20]}, type {self.type}'
