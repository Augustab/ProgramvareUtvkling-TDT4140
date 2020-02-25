from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect
from .models import Room
from .forms import DateForm

# Create your views here.

# denne var bare for å teste
def index(response):
    return HttpResponse("<h1>NY ENDRING</h1>")


# denne må vi ha, den tegner selve forsiden.
def home(response):
    return render(response, "../templates/forside.html")


# denne må vi ha, den tegner se_rom.
def se_rom(request):
    startdate = 0
    sluttdate = 0
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            startdate = form.cleaned_data['startdato']
            sluttdate = form.cleaned_data['sluttdato']

    available_rooms = Room.objects.filter(available=True)
    ##filtrer på dato og kapasitet i tillegg!!
    context = {'available_rooms': available_rooms}
    return render(request, "../templates/se_rom.html", context)


# Denne funksjonen sørger for at dersom du ikke har skrevet noe i url-en (dvs = "http://127.0.0.1:8000/") så skal du
# redirectes til http://127.0.0.1:8000/home/ dette fordi vi vil at brukerene skal være på hjem siden når man starter
# programmet.
def redirect(request):
    return HttpResponsePermanentRedirect(reverse('home'))
