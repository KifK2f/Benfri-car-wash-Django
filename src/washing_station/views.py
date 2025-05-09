from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.models import Service

@login_required
def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'services': services})