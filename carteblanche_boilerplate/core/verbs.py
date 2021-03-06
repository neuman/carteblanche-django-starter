from django.core.urlresolvers import reverse
from carteblanche.base import Noun
from carteblanche.mixins import DjangoVerb, availability_login_required

APPNAME = 'core'

class CoreVerb(DjangoVerb):
    app = APPNAME
    condition_name = 'is_public'
    success_message = 'You did it!'


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
    abstract class for all verbs only visible to users who are not authenticated
    '''
    condition_name = 'is_not_authenticated'
    required = True

    def is_available(self, user):
        #only available to non-logged in users
        if user.is_authenticated():
            return False
        return True


class SiteJoinVerb(NotAuthenticatedVerb):
    display_name = "Join This Site"
    view_name='user_create'


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

class SprocketListVerb(AuthenticatedVerb):
    display_name = "List Sprockets"
    view_name = 'sprocket_list'

class SiteRoot(Noun):
    '''
    A convenient hack that lets pages that have no actual noun have verbs and verb-based permissions. 
    '''
    verb_classes = [SiteJoinVerb, SiteLoginVerb, SprocketCreateVerb, SprocketListVerb]

    def __unicode__(self):
        return 'Site Root'

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
        return self.noun.is_sprocketeer(user)

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)


class SprocketUpdateVerb(SprocketeerVerb):
    display_name = "Update Sprocket"
    view_name = 'sprocket_update'


class SprocketDeleteVerb(SprocketeerVerb):
    display_name = "Delete Sprocket"
    view_name = 'sprocket_delete'


class SprocketDetailVerb(AuthenticatedVerb):
    display_name = "View Sprocket"
    view_name = 'sprocket_detail'

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)

