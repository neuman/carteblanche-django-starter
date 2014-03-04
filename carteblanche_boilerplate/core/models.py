from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from carteblanche.base import Noun
from core.verbs import *

class Sprocket(models.Model, Noun):
    sprocketeers = models.ManyToManyField(User)
    title = models.CharField(max_length=300)
    verb_classes = [SprocketDetailVerb, SprocketUpdateVerb, SprocketListVerb]

    def __str__(self):
        return self.title

    def is_sprocketeer(self, user):
        return self.sprocketeers.filter(id=user.id).count() > 0

    def get_absolute_url(self):
        return SprocketDetailVerb(self).get_url()
