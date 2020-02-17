from django.shortcuts import render
from django.template import context, loader

def forside(request):
    return render(request, '../templates/forside.html', {})

