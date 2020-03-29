'''Filen som tegner alle html-sidene.'''
import base64
import io
import urllib
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, reverse
from .forms import DateForm, BookingForm, CancelForm
from .models import Room, Booking
matplotlib.use('Agg')
# use Agg var noe som skulle hjelpe for å plotte grafene.

MONTH_DIC = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "Mai",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Okt",
    "Nov",
    "Des"]


def home(response):
    '''denne må vi ha, den tegner selve forsiden'''
    context = {
        'er_vaskehjelp': response.user.groups.filter(
            name='vaskehjelp').exists(),
        'er_investor': response.user.groups.filter(
            name='investor').exists()}
    plt.close(1)
    plt.close(2)
    return render(response, "../templates/forside.html", context)


def months_list():
    '''Funksjonen som brukes for å danne x-aksen på grafen (med måneder)'''
    dates = [datetime.today()]
    for i in range(11):
        i_x = dates[len(dates) - 1]
        try:
            nextmonthdate = i_x.replace(month=i_x.month + 1)
        except ValueError:
            if i_x.month == 12:
                nextmonthdate = i_x.replace(year=i_x.year + 1, month=1)
            else:
                nextmonthdate = i_x.replace(month=i_x.month + 1, day=i_x.day - 10)
        dates.append(nextmonthdate)
    string_dates = []
    for date in dates:
        string_dates.append(MONTH_DIC[date.month - 1])
    return string_dates


def statistikk(request):
    '''Funksjonen somm rendrer statistikksiden.'''
    plt.figure(2)
    plt.ylabel('Antall')
    plt.title('Antall bookinger i kommende måneder')
    plt.plot(months_list(), get_bookings_per_month())

    fig2 = plt.gcf()
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    string2 = base64.b64encode(buf2.read())
    uri2 = urllib.parse.quote(string2)
    return render(request, "../templates/statistikk.html",
                  {'data2': uri2, 'omsetning': get_omsetning()})


def vaskehjelp(response):
    '''Funksjonen som rendrer vaskehjelp-siden'''
    available_rooms = Room.objects.filter(available=True)
    context = {}
    room_nums = []
    for room in available_rooms:
        related_bookings = Booking.objects.filter(room=room)
        if related_bookings:
            room_nums.append(room.room_no)
            room.related_bookings = related_bookings

    context["room_nums"] = room_nums
    context["available_rooms"] = available_rooms
    print(context)
    return render(response, "../templates/se_vaskbare_rom.html", context)


def se_rom(request):
    '''Funksjonen som rendrer se rom siden'''
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
    if req_startdate is None or req_sluttdate is None or req_cap == 0:
        messages.warning(
            request,
            "Du må fylle inn alle feltene for å se tilgjengelige rom")
        return render(request, "../templates/forside.html")
    elif not check_legal_dates(req_startdate, req_sluttdate):
        messages.warning(request, "Datovalget ditt er ikke gyldig.")
        return render(request, "../templates/forside.html")
    else:
        available_rooms = Room.objects.filter(available=True)
        # Her går jeg gjennom de x antall romtypene, og setter prisen deres.
        for i_x in range(len(room_chars)):
            # henter ut de aktuelle rommene av denne typen
            assigned_rooms_type = list(
                Room.objects.filter(
                    room_type=room_chars[i_x]))
            try:
                # velger det første av disse aktuelle rommene, og henter prisen
                # til det rommet.
                prices[i_x] = assigned_rooms_type[0].price
            except BaseException:
                continue
        # sender de tre pris-verdiene inn i context. PRØVDE å sende
        # alle inn i en liste, men da klarer jeg ikke hente de
        # ut på html-siden.
        context = {
            'available_rooms': available_rooms,
            'req_startdate': req_startdate,
            'req_sluttdate': req_sluttdate,
            'req_cap': req_cap,
            'price1': prices[0],
            'price2': prices[1],
            'price3': prices[2]}
        return render(request, "../templates/se_rom.html", context)


def booking(request):
    '''Funksjonen som oppretter en booking.'''
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
                    # kjører så is_available for å kontrolleere overlappende
                    # bookinger.
                    if is_available(room, req_startdate, req_sluttdate):
                        # kommer du hit har du funnet et lovlig rom, lagrer
                        # rommet og stopper for-løkken.
                        allowed_room = room
                        break
            except BaseException:
                pass
            context = {
                'available_rooms': available_rooms,
                'req_startdate': req_startdate,
                'req_sluttdate': req_sluttdate,
                'req_room_type': req_room_type,
                'req_cap': 1,
                'user': request.user}
            if not check_legal_dates(req_startdate, req_sluttdate):
                messages.warning(request, "Datovalget ditt er ikke gyldig.")
                return render(request, "../templates/se_rom.html", context)
            elif allowed_room is not None:
                # Her oppretter jeg en ny booking med det lovlige rommet. !!!
                # User finner man med request.user !!!
                new_booking = Booking(
                    guest=request.user,
                    cin_date=req_startdate,
                    cout_date=req_sluttdate,
                    room_type=req_room_type,
                    room=allowed_room)
                new_booking.save()
                respons = "Thank you for booking with us at Skikkelig Fancy Hotell! Here are the reservation details:\nArrival:" + req_startdate + "\nCheckout:" + req_sluttdate + \
                    "\nBooking ID: 52768 – Room 3\n \nPlease make sure this information is correct. If not, please contact us as soon as possible to make necessary corrections at: \nEmail: skikkeligfancyhotell@gmail.com \nPhone: +11 1 1111 1000 \n\nWe look forward to welcoming you to Skikkelig Fancy Hotell. Check-in is after 4:00 PM; check-out time is 12:00 AM. \n\nBest regards, \nThe staff at Skikkelig Fancy Hotell!"
                send_mail('Order Confirmation',
                          respons,
                          'skikkeligfancyhotell@gmail.com',
                          [request.user.email],
                          fail_silently=False)
                messages.warning(request, "Booking vellykket.")
                return render(request, "../templates/se_rom.html", context)
            else:
                # om man ikke fant et rom kommer man hit,
                # da lager jeg en message om at det ikke gikk. Logikken for å
                # displaye messagen ligger i se_rom.html
                messages.warning(
                    request, "Det finnes ingen tilgjengelige rom i dette tilfellet.")
                return render(request, "../templates/se_rom.html", context)


def redirect(request):
    '''Redirecter deg til hjemmesiden dersom ikke noe er angitt i url'en'''
    return HttpResponsePermanentRedirect(reverse('home'))


def se_booking(request):
    '''Denne funksjonen rendrer se bestillinger-siden. '''
    # dette er viewen som sender deg til siden som viser dine bestillinger.
    # Først henter jeg ut brukeren.
    user = request.user
    # sender denne informasjonen inn som context
    context = {
        'related_bookings': Booking.objects.filter(
            guest=user),
        'user': user.username}
    return render(request, "../templates/se_bestillinger.html", context)


def slett_booking(request):
    '''Denne funksjonen sletter den valgte bookingen'''
    # som dere ser i se_bestillinger.html har vi en form som sender deg hit
    # ved buttontrykk.
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
                return render(
                    request,
                    "../templates/se_bestillinger.html",
                    context)
            else:
                # denne funksjonaliteten kjører om du ikke klarte å få tak i en
                # booking id.
                messages.warning(request, "Fikk ikke slettet rommet.")
                user = request.user
                related_bookings = Booking.objects.filter(guest=user)
                context = {'related_bookings': related_bookings}
                return render(
                    request,
                    "../templates/se_bestillinger.html",
                    context)


# funknjonen som ser etter overlappende bookinger.
def is_available(room, req_startdate, req_sluttdate):
    '''Dette er funksjonen som ser omnoen av de eksisterende
     bookingene på input-rommet krasjer med de foreslåttedatoene.'''
    # Check if the dates are valid case 1:
    #Denn sjekker dersom det finnes en rom-booking med sluttdato inni det
    # ønskede intervallet, men merk at det står gt siden
    # count_date=req_startdate går fint!!!
    case_1 = Booking.objects.filter(
        room=room,
        cout_date__gt=req_startdate,
        cout_date__lte=req_sluttdate).exists()
    # case 2: !!!! Denn sjekker dersom det finnes
    # en rom-booking med startdato inni det ønskede intervallet,
    # men merk at det står lt siden cin_date=req_sluttdate går fint!!!
    case_2 = Booking.objects.filter(
        room=room,
        cin_date__gte=req_startdate,
        cin_date__lt=req_sluttdate).exists()
    # case 3: !!! denne ser om det er en roombooking som omslutter den
    # requestede!
    case_3 = Booking.objects.filter(
        room=room,
        cout_date__lte=req_startdate,
        cout_date__gte=req_sluttdate).exists()
    # om en av casene existerer er det en krasj i bookingen.
    if case_1 or case_2 or case_3:
        return False
    else:
        return True


def check_legal_dates(startdate, sluttdate):
    '''Sjekker om to datoer er gyldige (eks ikke slutt før start)'''
    return datetime.strftime(
        datetime.today(),
        '%Y-%m-%d') <= startdate < sluttdate


def get_omsetning():
    '''kalkulerer total omsetning for alle bookinger ved
    å gange pris.pr.natt med antall netter'''
    bookings = Booking.objects.all()
    omsetning = 0
    for booking in bookings:
        daydif = booking.cout_date - booking.cin_date
        omsetning += daydif.days * int(booking.room.price)
    return omsetning


def get_bookings_per_month():
    '''Funksjon som returnerer en liste med antall bookinger i kommende
    månedder, der posisjonen i listen er gitt av hvilken måned vi er i nå
    og dermed er første indeks = måneden vi er i nå.'''
    dates = [datetime.today()]
    for i in range(11):
        i_x = dates[len(dates) - 1]
        try:
            nextmonthdate = i_x.replace(month=i_x.month + 1)
        except ValueError:
            if i_x.month == 12:
                nextmonthdate = i_x.replace(year=i_x.year + 1, month=1)
            else:
                nextmonthdate = i_x.replace(month=i_x.month + 1, day=i_x.day - 10)
        dates.append(nextmonthdate)
    bookings = Booking.objects.all()
    count_bookings = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for booking in bookings:
        count_bookings[booking.cin_date.month - 1] += 1
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(dates) - 1):
        result[i] = count_bookings[dates[i].month - 1]
    return result
