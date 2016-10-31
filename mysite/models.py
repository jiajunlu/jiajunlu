from django.db import models


class Card24Game_SavedAnswer(models.Model):
    question = models.CharField(max_length=30)
    incache = models.BooleanField()


class Card24Game(models.Model):
    question = models.CharField(max_length=30)
    answer = models.CharField(max_length=30)
