from django.shortcuts import render
from django.template import context, loader
from django.http import HttpResponse


def forside(request):
    return HttpResponse('hei')
    #return render(request, '../templates/forside.html', {})  # se på denne, templatesfolderen er ikke den i 36
