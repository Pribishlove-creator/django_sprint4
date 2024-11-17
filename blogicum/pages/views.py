from django.views.generic import TemplateView
from django.shortcuts import render

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class RulesView(TemplateView):
    template_name = 'pages/rules.html'

def csrf_error_view(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)

def page_not_found_view(request, exception=None):
    return render(request, 'pages/404.html', status=404)

def server_error_view(request):
    return render(request, 'pages/500.html', status=500)
