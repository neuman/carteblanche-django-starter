from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import DetailView
from django.contrib.auth.models import User
from carteblanche.mixins import NounView

import core.models as cm
import core.forms as cf

# Create your views here.

class SiteRootView(NounView):
    def get_noun(self, **kwargs):
        siteroot = cm.SiteRoot()
        return siteroot

class IndexView(SiteRootView, TemplateView):
    template_name = 'bootstrap.html'

class UserCreateView(SiteRootView, CreateView):
    model = User
    template_name = 'form.html'
    form_class = cf.RegistrationForm

    def form_valid(self, form):
        user = User.objects.create_user(uuid4().hex, form.cleaned_data['email'], form.cleaned_data['password1'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['first_name']
        user.save()
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        login(self.request, user)
        form.instance = user
        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        action.send(self.request.user, verb='joined', action_object=self.object)
        return reverse(viewname='user_detail', args=(self.object.id,), current_app='core')

class UserLoginView(SiteRootView, FormView):
    template_name = 'form.html'
    form_class = cf.LoginForm

    def form_valid(self, form):
        user = form.user_cache
        login(self.request, user)
        form.instance = user
        return super(UserLoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse(viewname='user_detail', args=(self.object.id,), current_app='core')     

class SprocketCreateView(SiteRootView, CreateView):
    model = cm.Sprocket
    template_name = 'form.html'
    form_class = cf.SprocketForm
    success_url = '/'

    def get_success_url(self):
        self.object.sprocketeers.add(self.request.user)
        return cm.SprocketDetailVerb(self.noun).get_url()

class SprocketView(NounView):
    def get_noun(self, **kwargs):
        return cm.Project.objects.get(id=self.kwargs['instance_id'])

class SprocketDetailView(SprocketView, TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['project'] = self.noun
        context['total_pledged'] = self.noun.get_total_pledged()
        return context

class SprocketUpdateView(SprocketView, UpdateView):
    model = cm.Sprocket
    template_name = 'form.html'
    success_url = '/'