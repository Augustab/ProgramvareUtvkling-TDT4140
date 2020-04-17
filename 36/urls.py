"""36 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import signup.views as v
import main.views as v2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', v.signup, name="signup"),
    path('home/', v2.home, name="home"),
    path('se_rom/', v2.se_rom, name="se_rom"),
    path("booking/", v2.booking, name="booking"),
    path("se_bestillinger/", v2.se_booking, name="se_bestillinger"),
    path("slett_booking/", v2.slett_booking, name="slett_booking"),
    path("vaskehjelp/", v2.vaskehjelp, name="vaskehjelp"),
    path("statistikk", v2.statistikk, name="statistikk"),
    path('', v2.redirect, name="homeredirectfraingenting"),
    path('', include("django.contrib.auth.urls")),
]