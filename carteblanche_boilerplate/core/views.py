from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import DetailView
from django.contrib.auth.models import User
#from carteblanche.mixins import NounView
from mixins import NounView
from django.contrib.auth import authenticate, login

import core.models as cm
import core.forms as cf

# Create your views here.

class SiteRootView(NounView):
    def get_noun(self, **kwargs):
        siteroot = cm.SiteRoot()
        return siteroot

class IndexView(SiteRootView, TemplateView):
    template_name = 'base.html'

#this login/user create stuff might be better off in a different app
class UserCreateView(SiteRootView, CreateView):
    model = User
    template_name = 'form.html'
    form_class = cf.RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        user = User.objects.create_user(uuid4().hex, form.cleaned_data['email'], form.cleaned_data['password1'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['first_name']
        user.save()
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        login(self.request, user)
        form.instance = user
        return super(UserCreateView, self).form_valid(form)


class UserLoginView(SiteRootView, FormView):
    template_name = 'form.html'
    form_class = cf.LoginForm
    success_url = '/'

    def form_valid(self, form):
        user = form.user_cache
        login(self.request, user)
        form.instance = user
        return super(UserLoginView, self).form_valid(form)    

class SprocketCreateView(SiteRootView, CreateView):
    model = cm.Sprocket
    template_name = 'form.html'
    form_class = cf.SprocketForm
    success_url = '/'

    def get_success_url(self):
        self.object.sprocketeers.add(self.request.user)
        return cm.SprocketDetailVerb(self.object).get_url()

class SprocketView(NounView):
    form_class = cf.SprocketForm

    def get_noun(self, **kwargs):
        return cm.Sprocket.objects.get(id=self.kwargs['pk'])

class SprocketDetailView(SprocketView, TemplateView):
    template_name = 'base.html'

class SprocketUpdateView(SprocketView, UpdateView):
    model = cm.Sprocket
    template_name = 'form.html'
    success_url = '/'

    def get_success_url(self):
        return cm.SprocketDetailVerb(self.noun).get_url()