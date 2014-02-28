from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from carteblanche.base import Noun
from carteblanche.django import DjangoVerb

# Create your models here.

APPNAME = 'core'

class CoreVerb(DjangoVerb):
    app = APPNAME
    condition_name = 'public'


class SiteJoinVerb(UnauthenticatedOnlyVerb):
    display_name = "Join Indiepen"
    view_name='user_ceate'


class SiteLoginVerb(UnauthenticatedOnlyVerb):
    display_name = "Login"
    view_name='user_login'


class SiteRoot(Noun):
    '''
    A hack that lets pages that have no actual noun have verbs and verb-based permissions. 
    '''
    verb_classes = [ProjectCreateVerb, SiteJoinVerb, SiteLoginVerb]

    class Meta:
        abstract = True

class UnauthenticatedOnlyVerb(CoreVerb):
    condition_name = 'is_unauthenticated'
    required = True

    def is_available(self, user):
        #only available to non-logged in users
        if user.is_authenticated():
            return False
        return True

class ProjectSprocketVerb(CoreVerb):
    display_name = "Create New Sprocket"
    view_name='sprocket_create'
    condition_name = 'is_authenticated'
    required = True

    @availability_login_required
    def is_available(self, user):
        return True

class Sprocket(Model, Noun):
	sprocketeers = models.ManyToManyField(User)
	title = models.CharField(max_length=300)
	verb_classes = [SprocketDetailVerb, SprocketUpdateVerb]