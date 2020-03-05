from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import messages
from .models import Room, Booking
from .forms import DateForm, BookingForm, CancelForm


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
    prices = [2000, 3000, 4000]
    room_chars = ["S", "D", "F"]
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            req_startdate = form.data.get('req_startdate')
            req_sluttdate = form.data.get('req_sluttdate')
            req_cap = int(form.data.get('req_cap'))
    available_rooms = Room.objects.filter(available=True)
    for ix in range(len(room_chars)):
        assigned_rooms_type = list(Room.objects.filter(room_type=room_chars[ix]))
        try:
            prices[ix] = assigned_rooms_type[0].price
        except:
            continue

    ##Room.capacity > int(req_cap)
    ##filtrer på dato og kapasitet i tillegg!!
    context = {'available_rooms': available_rooms, 'req_startdate': req_startdate, 'req_sluttdate': req_sluttdate,
               'req_cap': req_cap, 'price1': prices[0], 'price2': prices[1], 'price3': prices[2]}
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
            available_rooms = Room.objects.filter(available=True)
            assigned_rooms = list(Room.objects.filter(room_type=req_room_type))
            allowed_room = None
            try:
                for room in assigned_rooms:
                    if is_available(room, req_startdate, req_sluttdate):
                        allowed_room = room
                        break
            except:
                pass

            context = {'available_rooms': available_rooms, 'req_startdate': req_startdate, 'req_sluttdate': req_sluttdate,
                       'req_room_type': req_room_type,
                       'req_cap': 1}

            if allowed_room is not None:
                new_booking = Booking(guest=request.user, cin_date=req_startdate, cout_date=req_sluttdate,
                                      room_type=req_room_type, room=allowed_room)
                new_booking.save()

                return render(request, "../templates/se_rom.html", context)
            else:
                messages.warning(request, "Det finnes ingen tilgjengelige rom i dette tilfellet.")
                return render(request, "../templates/se_rom.html", context)


# Denne funksjonen sørger for at dersom du ikke har skrevet noe i url-en (dvs = "http://127.0.0.1:8000/") så skal du
# redirectes til http://127.0.0.1:8000/home/ dette fordi vi vil at brukerene skal være på hjem siden når man starter
# programmet.

def redirect(request):
    return HttpResponsePermanentRedirect(reverse('home'))


def se_booking(request):
    user = request.user
    related_bookings = Booking.objects.filter(guest=user)
    context = {'related_bookings': related_bookings, 'user': user.username}
    return render(request, "../templates/se_bestillinger.html", context)


def slett_booking(request):
    if request.method == "POST":
        form = CancelForm(request.POST)
        if form.is_valid():
            bookingid = form.data.get('bookingid')
            if bookingid is not None:
                Booking.objects.get(bookingid=bookingid).delete()
                user = request.user
                related_bookings = Booking.objects.filter(guest=user)
                context = {'related_bookings': related_bookings}
                return render(request, "../templates/se_bestillinger.html", context)
            else:
                messages.warning(request, "Fikk ikke slettet rommet.")
                user = request.user
                related_bookings = Booking.objects.filter(guest=user)
                context = {'related_bookings': related_bookings}
                return render(request, "../templates/se_bestillinger.html", context)


def is_available(room, req_startdate, req_sluttdate):
    # Check if the dates are valid
    # case 1: a room is booked before the check_in date, and checks out after the requested check_in date
    case_1 = Booking.objects.filter(room=room,  cout_date__gt=req_startdate, cout_date__lte=req_sluttdate).exists()

    # case 2: a room is booked before the requested check_out date and check_out date is after requested check_out date
    case_2 = Booking.objects.filter(room=room, cin_date__gte=req_startdate, cin_date__lt=req_sluttdate).exists()

    # case 3: check if requested checkin and checkout is "inside" a reservation
    case_3 = Booking.objects.filter(room=room, cout_date__lte=req_startdate, cout_date__gte=req_sluttdate).exists()
    if case_1 or case_2 or case_3:
        return False
    else:
        return True
