from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect
from .models import Room, Booking
from .forms import DateForm, BookingForm

# Create your views here.

# denne var bare for å teste
def index(request):

    return HttpResponse("hei")



# denne må vi ha, den tegner selve forsiden.
def home(response):
    return render(response, "../templates/forside.html")


# denne må vi ha, den tegner se_rom.
def se_rom(request):
    req_startdate = 0
    req_sluttdate = 0
    req_cap = 0
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            req_startdate = form.data.get('req_startdate')
            req_sluttdate = form.data.get('req_sluttdate')
            req_cap = int(form.data.get('req_cap'))
    available_rooms = Room.objects.filter(available=True)
    ##Room.capacity > int(req_cap)
    ##filtrer på dato og kapasitet i tillegg!!
    context = {'available_rooms': available_rooms, 'req_startdate': req_startdate, 'req_sluttdate': req_sluttdate, 'req_cap': req_cap}
    return render(request, "../templates/se_rom.html", context)



def booking(request):
    req_startdate = 0
    req_sluttdate = 0
    req_room_type = 0
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            req_startdate = form.data.get('req_startdate')
            req_sluttdate = form.data.get('req_sluttdate')
            req_room_type = form.data.get('req_room_type')



            new_booking = Booking(guest = request.user, cin_date = req_startdate, cout_date = req_sluttdate, room_type = req_room_type)
            new_booking.save()
    context = {'req_startdate': req_startdate, 'req_sluttdate': req_sluttdate, 'req_room_type': req_room_type, 'req_cap': 1}
    return render(request, "../templates/se_rom.html", context)
    '''
                return redirect("/reservation_success", context)
            else:
                return redirect("/reservation_fail")'''

# Denne funksjonen sørger for at dersom du ikke har skrevet noe i url-en (dvs = "http://127.0.0.1:8000/") så skal du
# redirectes til http://127.0.0.1:8000/home/ dette fordi vi vil at brukerene skal være på hjem siden når man starter
# programmet.
def redirect(request):
    return HttpResponsePermanentRedirect(reverse('home'))
