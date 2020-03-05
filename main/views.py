from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import messages
from .models import Room, Booking
from .forms import DateForm, BookingForm, CancelForm


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
    # Her går jeg gjennom de x antall romtypene, og setter prisen deres.
    for ix in range(len(room_chars)):
        # henter ut de aktuelle rommene av denne typen
        assigned_rooms_type = list(Room.objects.filter(room_type=room_chars[ix]))
        try:
            # velger det første av disse aktuelle rommene, og henter prisen til det rommet.
            prices[ix] = assigned_rooms_type[0].price
        except:
            continue
    # sender de tre pris-verdiene inn i context. PRØVDE å sende alle inn i en liste, men da klarer jeg ikke hente de
    # ut på html-siden.
    context = {'available_rooms': available_rooms, 'req_startdate': req_startdate, 'req_sluttdate': req_sluttdate,
               'req_cap': req_cap, 'price1': prices[0], 'price2': prices[1], 'price3': prices[2]}
    return render(request, "../templates/se_rom.html", context)


def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            req_startdate = form.data.get('req_startdate')
            req_sluttdate = form.data.get('req_sluttdate')
            req_room_type = form.data.get('req_room_type')
            available_rooms = Room.objects.filter(available=True)
            # henter alle rom av room_typen som er ønsket av kunden
            assigned_rooms = list(Room.objects.filter(room_type=req_room_type))
            # denne variabelen brukes for å lagre et lovlig rom
            allowed_room = None
            try:
                # itererer gjennom roomene som er aktuelle (riktig type)
                for room in assigned_rooms:
                    # kjører så is_available for å kontrolleere overlappende bookinger.
                    if is_available(room, req_startdate, req_sluttdate):
                        # kommer du hit har du funnet et lovlig rom, lagrer rommet og stopper for-løkken.
                        allowed_room = room
                        break
            except:
                pass

            context = {'available_rooms': available_rooms, 'req_startdate': req_startdate,
                       'req_sluttdate': req_sluttdate,
                       'req_room_type': req_room_type,
                       'req_cap': 1}

            if allowed_room is not None:
                # Her oppretter jeg en ny booking med det lovlige rommet. !!! User finner man med request.user !!!
                new_booking = Booking(guest=request.user, cin_date=req_startdate, cout_date=req_sluttdate,
                                      room_type=req_room_type, room=allowed_room)
                new_booking.save()

                return render(request, "../templates/se_rom.html", context)
            else:
                # om man ikke fant et rom kommer man hit, da lager jeg en message om at det ikke gikk. Logikken for å
                # displaye messagen ligger i se_rom.html
                messages.warning(request, "Det finnes ingen tilgjengelige rom i dette tilfellet.")
                return render(request, "../templates/se_rom.html", context)


# Denne funksjonen sørger for at dersom du ikke har skrevet noe i url-en (dvs = "http://127.0.0.1:8000/") så skal du
# redirectes til http://127.0.0.1:8000/home/ dette fordi vi vil at brukerene skal være på hjem siden når man starter
# programmet.
def redirect(request):
    return HttpResponsePermanentRedirect(reverse('home'))


def se_booking(request):
    # dette er viewen som sender deg til siden som viser dine bestillinger. Først henter jeg ut brukeren.
    user = request.user
    # henter relaterte bookinger til brukeren
    related_bookings = Booking.objects.filter(guest=user)
    # sender denne informasjonen inn som context
    context = {'related_bookings': related_bookings, 'user': user.username}
    return render(request, "../templates/se_bestillinger.html", context)


def slett_booking(request):
    # som dere ser i se_bestillinger.html har vi en form som sender deg hit ved buttontrykk.
    if request.method == "POST":
        form = CancelForm(request.POST)
        if form.is_valid():
            # bookingid henter jeg fra det SKJULTE INPUTFELTET I FORM'en.
            bookingid = form.data.get('bookingid')
            if bookingid is not None:
                # sletter den valgte bookingen
                Booking.objects.get(bookingid=bookingid).delete()
                user = request.user
                # henter ut den oppdaterte listen over brukerens bookinger
                related_bookings = Booking.objects.filter(guest=user)
                context = {'related_bookings': related_bookings}
                return render(request, "../templates/se_bestillinger.html", context)
            else:
                # denne funksjonaliteten kjører om du ikke klarte å få tak i en booking id.
                messages.warning(request, "Fikk ikke slettet rommet.")
                user = request.user
                related_bookings = Booking.objects.filter(guest=user)
                context = {'related_bookings': related_bookings}
                return render(request, "../templates/se_bestillinger.html", context)


# funknjonen som ser etter overlappende bookinger.
def is_available(room, req_startdate, req_sluttdate):
    # Check if the dates are valid case 1: !!!! Denn sjekker dersom det finnes en rom-booking med sluttdato inni det
    # ønskede intervallet, men merk at det står gt siden count_date=req_startdate går fint!!!
    case_1 = Booking.objects.filter(room=room, cout_date__gt=req_startdate, cout_date__lte=req_sluttdate).exists()

    # case 2: !!!! Denn sjekker dersom det finnes en rom-booking med startdato inni det ønskede intervallet,
    # men merk at det står lt siden cin_date=req_sluttdate går fint!!!
    case_2 = Booking.objects.filter(room=room, cin_date__gte=req_startdate, cin_date__lt=req_sluttdate).exists()

    # case 3: !!! denne ser om det er en roombooking som omslutter den requestede!
    case_3 = Booking.objects.filter(room=room, cout_date__lte=req_startdate, cout_date__gte=req_sluttdate).exists()

    # om en av casene existerer er det en krasj i bookingen.
    if case_1 or case_2 or case_3:
        return False
    else:
        return True
