from django.shortcuts import render
from django.views.generic import ListView, DetailView
from services.models import Service

# Create your views here.
class ServiceHome(ListView):
    model = Service
    context_object_name = "services"

class ServiceDetail(DetailView):
    model = Service
    context_object_name = "service"
    # template_name = "blog_post_detail.html" -- optinel
