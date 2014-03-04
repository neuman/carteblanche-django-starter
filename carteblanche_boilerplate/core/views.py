from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import DetailView
from django.contrib.auth.models import User
from carteblanche.mixins import NounView
from django.contrib.auth import authenticate, login

import core.models as cm
import core.forms as cf

class SiteRootView(NounView):
    def get_noun(self, **kwargs):
        siteroot = cm.SiteRoot()
        return siteroot

class IndexView(SiteRootView, TemplateView):
    template_name = 'index.html'

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

from django.core.urlresolvers import resolve
   
class SprocketListlView(SiteRootView, ListView):
    template_name = 'base.html'

    def get_url_name(self):
        return resolve(self.request.path_info).url_name

    def get_verb_display_name(self):
        return self.get_view_required_verbs(self.get_url_name())[0].display_name

    def get_context_data(self, **kwargs):
        context = super(SprocketListlView, self).get_context_data(**kwargs)
        #raise Exception(self.noun.get_verbs())
        context['verb_display_name'] = self.get_verb_display_name()
        return context

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        else:
            queryset = cm.Sprocket.objects.all()
        return queryset

class SprocketUpdateView(SprocketView, UpdateView):
    model = cm.Sprocket
    template_name = 'form.html'
    success_url = '/'

    def get_success_url(self):
        return cm.SprocketDetailVerb(self.noun).get_url()