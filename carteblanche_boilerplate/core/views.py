from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import DetailView

# Create your views here.

class SiteRootView(NounView):
    def get_noun(self, **kwargs):
        siteroot = cm.SiteRoot()
        return siteroot

class IndexView(SiteRootView, TemplateView):
    template_name = 'bootstrap.html'

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

class PostUpdateView(SprocketView, UpdateView):
    model = cm.Post
    template_name = 'form.html'
    success_url = '/'

    def get_form(self, form_class):
        return cf.PostForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        form.instance.changed_by = self.request.user
        return super(PostCreateView, self).form_valid(form)