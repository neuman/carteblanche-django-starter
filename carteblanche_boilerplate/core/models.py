from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from carteblanche.base import Noun
from carteblanche.mixins import DjangoVerb, availability_login_required

# Create your models here.

APPNAME = 'core'

class CoreVerb(DjangoVerb):
    app = APPNAME
    condition_name = 'is_public'

class AuthenticatedVerb(CoreVerb):
    '''
    abstract class for all verbs only visible to authenticated users
    '''
    condition_name = 'is_authenticated'
    required = True

    def is_available(self, user):
        return user.is_authenticated()

class NotAuthenticatedVerb(CoreVerb):
    '''
    abstract class for all verbs only visible to not authenticated users
    '''
    condition_name = 'is_not_authenticated'
    required = True

    def is_available(self, user):
        #only available to non-logged in users
        if user.is_authenticated():
            return False
        return True

class SiteJoinVerb(NotAuthenticatedVerb):
    display_name = "Join Indiepen"
    view_name='user_ceate'

class SiteLoginVerb(NotAuthenticatedVerb):
    display_name = "Login"
    view_name='user_login'

class SprocketCreateVerb(CoreVerb):
    display_name = "Create New Sprocket"
    view_name='sprocket_create'
    condition_name = 'is_authenticated'
    required = True

    @availability_login_required
    def is_available(self, user):
        return True

class SiteRoot(Noun):
    '''
    A convenient hack that lets pages that have no actual noun have verbs and verb-based permissions. 
    '''
    verb_classes = [SiteJoinVerb, SiteLoginVerb, SprocketCreateVerb]

    class Meta:
        abstract = True


class SprocketeerVerb(CoreVerb):
    '''
    abstract class for all verbs available only to a sprocket's sprocketeers
    '''
    denied_message = "You must be one of the sprocket's sprocketeers to upload to this post."
    condition_name = "is_sprocketeer"

    @availability_login_required
    def is_available(self, user):
        return self.noun.sprocketeers.filter(id=user.id).count() > 0

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)


class SprocketUpdateVerb(SprocketeerVerb):
    display_name = "Upload Post Files"
    view_name = 'post_media_uploads'


class SprocketDeleteVerb(SprocketeerVerb):
    display_name = "Upload a File"
    view_name = 'post_media_create'
    visible = False


class SprocketDetailVerb(CoreVerb):
    display_name = "View Post"
    view_name = 'post_detail'
    condition_name = "can_view"
    required = True
    denied_message = "Sorry, that post isn't published yet."

    def is_available(self, user):
        if self.noun.is_published():
            return True
        elif self.noun.project.members.filter(id=user.id).count() > 0:
                return True
        else:
            return False

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)


class Sprocket(models.Model, Noun):
    sprocketeers = models.ManyToManyField(User)
    title = models.CharField(max_length=300)
    verb_classes = [SprocketDetailVerb, SprocketUpdateVerb, SprocketDeleteVerb]
