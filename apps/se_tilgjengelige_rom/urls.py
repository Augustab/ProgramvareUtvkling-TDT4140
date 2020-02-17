from django.urls import path
from . import views #views i se_tilgjengelige_rom

urlpatterns = [path('', views.forside, name= 'forside'), #en path til forside i se_tilgjengelige_rom/views.py
               ]
