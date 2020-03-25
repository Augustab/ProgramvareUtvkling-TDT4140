import signup.views as v
from django.core.mail import send_mail
from datetime import datetime, timedelta
from signup.forms import RegisterForm
from .forms import DateForm, BookingForm, CancelForm
from .models import Room, Booking
from django.contrib import messages
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, reverse
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt
import base64
import io
import urllib
import numpy as np
import matplotlib
matplotlib.use('Agg')

month_dic = [
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


'''
def get_omsetning_plot():
    omsetning = get_omsetning()

    objects = ['Omsetning']
    y_pos = np.arange(len(objects))
    performance = [omsetning]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('NOK')
    plt.title('Total Omsetning (planlagt)')

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

def get_months_plot():
    plt2.ylabel('Antall')
    plt2.title('Antall bookinger i kommende måneder')
    plt2.plot([1, 2, 3, 4], [1, 4, 9, 16])

    fig2 = plt2.gcf()
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    string2 = base64.b64encode(buf2.read())
    uri2 = urllib.parse.quote(string2)
    return uri2
'''


def months_list():
    dates = [datetime.today()]
    for i in range(11):
        x = dates[len(dates) - 1]
        try:
            nextmonthdate = x.replace(month=x.month + 1)
        except ValueError:
            if x.month == 12:
                nextmonthdate = x.replace(year=x.year + 1, month=1)
            else:
                nextmonthdate = x.replace(month=x.month + 1, day=x.day - 10)
        dates.append(nextmonthdate)
    string_dates = []
    for i in range(0, len(dates)):
        string_dates.append(month_dic[dates[i].month - 1])
    return string_dates


def get_bookings_per_month():
    dates = [datetime.today()]
    for i in range(11):
        x = dates[len(dates) - 1]
        try:
            nextmonthdate = x.replace(month=x.month + 1)
        except ValueError:
            if x.month == 12:
                nextmonthdate = x.replace(year=x.year + 1, month=1)
            else:
                nextmonthdate = x.replace(month=x.month + 1, day=x.day - 10)
        dates.append(nextmonthdate)
    bookings = Booking.objects.all()
    count_bookings = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for booking in bookings:
        count_bookings[booking.cin_date.month - 1] += 1
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(dates) - 1):
        result[i] = count_bookings[dates[i].month - 1]
    return result


def statistikk(request):
    '''
    x1 = np.linspace(0.0, 5.0)
    x2 = np.linspace(0.0, 2.0)

    y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
    y2 = np.cos(2 * np.pi * x2)

    plt.subplot(2, 1, 1)
    plt.plot(x1, y1, 'o-')
    plt.title('Statistikk for skikkelig fancy hotell')
    plt.ylabel('Damped oscillation')

    plt.subplot(2, 1, 2)
    plt.plot(x2, y2, '.-')
    plt.xlabel('time (s)')
    plt.ylabel('Undamped')

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    '''

    omsetning = get_omsetning()

    objects = ['Omsetning']
    plt.figure(1)
    y_pos = np.arange(len(objects))
    performance = [omsetning]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('NOK')
    plt.title('Total Omsetning (planlagt)')

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    # figure 2 under!
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
                  {'data1': uri, 'data2': uri2})


def vaskehjelp(response):
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
        for ix in range(len(room_chars)):
            # henter ut de aktuelle rommene av denne typen
            assigned_rooms_type = list(
                Room.objects.filter(
                    room_type=room_chars[ix]))
            try:
                # velger det første av disse aktuelle rommene, og henter prisen
                # til det rommet.
                prices[ix] = assigned_rooms_type[0].price
            except BaseException:
                continue
        # sender de tre pris-verdiene inn i context. PRØVDE å sende alle inn i en liste, men da klarer jeg ikke hente de
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
                # om man ikke fant et rom kommer man hit, da lager jeg en message om at det ikke gikk. Logikken for å
                # displaye messagen ligger i se_rom.html
                messages.warning(
                    request, "Det finnes ingen tilgjengelige rom i dette tilfellet.")
                return render(request, "../templates/se_rom.html", context)


# Denne funksjonen sørger for at dersom du ikke har skrevet noe i url-en (dvs = "http://127.0.0.1:8000/") så skal du
# redirectes til http://127.0.0.1:8000/home/ dette fordi vi vil at brukerene skal være på hjem siden når man starter
# programmet.
def redirect(request):
    return HttpResponsePermanentRedirect(reverse('home'))


def se_booking(request):
    # dette er viewen som sender deg til siden som viser dine bestillinger.
    # Først henter jeg ut brukeren.
    user = request.user
    # henter relaterte bookinger til brukeren
    related_bookings = Booking.objects.filter(guest=user)
    # sender denne informasjonen inn som context
    context = {'related_bookings': related_bookings, 'user': user.username}
    return render(request, "../templates/se_bestillinger.html", context)


def slett_booking(request):
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
    # Check if the dates are valid case 1: !!!! Denn sjekker dersom det finnes en rom-booking med sluttdato inni det
    # ønskede intervallet, men merk at det står gt siden
    # count_date=req_startdate går fint!!!
    case_1 = Booking.objects.filter(
        room=room,
        cout_date__gt=req_startdate,
        cout_date__lte=req_sluttdate).exists()
    # case 2: !!!! Denn sjekker dersom det finnes en rom-booking med startdato inni det ønskede intervallet,
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
    return datetime.strftime(
        datetime.today(),
        '%Y-%m-%d') <= startdate < sluttdate


def get_omsetning():
    bookings = Booking.objects.all()
    omsetning = 0
    for booking in bookings:
        daydif = booking.cout_date - booking.cin_date
        omsetning += daydif.days * int(booking.room.price)
    return omsetning
