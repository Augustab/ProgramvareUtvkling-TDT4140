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
    req_startdate = 0
    req_sluttdate = 0
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            req_startdate = form.cleaned_data['req_startdato']
            req_sluttdate = form.cleaned_data['req_sluttdato']
            req_cap = form.cleaned_data['req_cap']

    available_rooms = Room.objects.filter(available=True)
    ##filtrer på dato og kapasitet i tillegg!!
    context = {'available_rooms': available_rooms, 'req_startdate': req_startdate, 'req_sluttdate': req_sluttdate}
    return render(request, "../templates/se_rom.html", context)

def booking(request):
    return HttpResponse("ssfgk")

# Denne funksjonen sørger for at dersom du ikke har skrevet noe i url-en (dvs = "http://127.0.0.1:8000/") så skal du
# redirectes til http://127.0.0.1:8000/home/ dette fordi vi vil at brukerene skal være på hjem siden når man starter
# programmet.
def redirect(request):
    return HttpResponsePermanentRedirect(reverse('home'))
