from io import BytesIO
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from mainapp.models import Tickets
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@login_required
def main(request):
    try:
        context = {
            'content': []
        }
        for content in Tickets.objects.filter(user_id=request.user.id).order_by('date_start'):
            context['content'].append(
                {'date': content.date_start, 'ticket': '',
                'country': content.country, 'id': content.id, 'price': content.price})
        return render(request, 'main.html', context=context)
    except Exception as e:
        context = {
            'error': "Something went wrong."
        }
        return render(request, 'main.html', context=context)


@login_required
def add_trip(request):
    return render(request, 'add_trip.html')


@swagger_auto_schema(
    method='post',
    operation_description="Получить данные с параметрами",
    manual_parameters=[
        openapi.Parameter('param', openapi.IN_QUERY, description="Пример параметра", type=openapi.TYPE_STRING)
    ],
    responses={200: openapi.Response('Success')},
)
@api_view(['POST'])
@login_required
def request_process_add_trip(request):
    if request.method == 'POST':
        try:
            country = request.POST['country']
            date_trip = request.POST['date_start']
            date_end_trip = request.POST['date_end']
            price = request.POST['price']
            trip_plan = request.POST['trip_plan']
            file_upload = request.FILES['file']
            if datetime.strptime(date_end_trip, "%Y-%m-%d").date() < datetime.strptime(date_trip, "%Y-%m-%d").date():
                return Response({'Status': 400})
            if country and date_trip and file_upload and price:
                file_read = file_upload.read()
                trip = Tickets.objects.create(user_id=request.user.id, country=country, date_start=date_trip, date_end=date_end_trip, ticket=file_read, price=price, trip_plan=trip_plan)
                trip.save()
                return Response({'Status': 200})
            return Response({'Status': 400})
        except Exception as e:
            print(e)
            context = {
                'error': "Something went wrong."
            }
            return Response(context)


@login_required
def process_add_trip(request):
    if request.method == 'POST':
        try:
            country = request.POST['country']
            date_trip = request.POST['date_start']
            date_end_trip = request.POST['date_end']
            price = request.POST['price']
            trip_plan = request.POST['trip_plan']
            file_upload = request.FILES['file']
            if datetime.strptime(date_end_trip, "%Y-%m-%d").date() < datetime.strptime(date_trip, "%Y-%m-%d").date():
                return render(request, 'add_trip.html', context={'error': "Дата начала должна быть раньше даты конца!"})
            if country and date_trip and file_upload and price:
                file_read = file_upload.read()
                trip = Tickets.objects.create(user_id=request.user.id, country=country, date_start=date_trip, date_end=date_end_trip, ticket=file_read, price=price, trip_plan=trip_plan)
                trip.save()
                return redirect('mainapp:main')
            return render(request, 'add_trip.html', context={'error': 'Не все поля заполнены!'})
        except Exception as e:
            print(e)
            context = {
                'error': "Something went wrong."
            }
            return render(request, 'add_trip.html', context=context)

@login_required
def download(request, id):
    ticket = get_object_or_404(Tickets, id=id, user_id=request.user.id)
    io_file = BytesIO(ticket.ticket or b'')
    response = FileResponse(io_file, content_type='application/pdf', filename='ticket.pdf')
    return response

ACHIEVEMENTS = [
    {'name': 'Начинающий Паспарту', 'threshold': 1, 'icon': '🌱',
     'desc': 'Посетите первую страну'},
    {'name': 'Продвинутый Паспарту', 'threshold': 5, 'icon': '🧭',
     'desc': 'Посетите 5 стран'},
    {'name': 'Эксперт Паспарту', 'threshold': 10, 'icon': '🏆',
     'desc': 'Посетите 10 стран'},
]


def visited_countries_count(user_id):
    """Число уникальных стран из уже состоявшихся поездок."""
    return (Tickets.objects
            .filter(user_id=user_id, date_start__lt=date.today())
            .values('country').distinct().count())


def build_achievements(count_country):
    """Лестница достижений с отметкой полученных и прогрессом до следующего."""
    ladder = []
    for a in ACHIEVEMENTS:
        ladder.append({**a, 'unlocked': count_country >= a['threshold']})

    unlocked = [a for a in ladder if a['unlocked']]
    current = unlocked[-1]['name'] if unlocked else 'Пока нет достижений'
    next_locked = next((a for a in ladder if not a['unlocked']), None)
    next_info = None
    if next_locked:
        remaining = next_locked['threshold'] - count_country
        next_info = {
            'name': next_locked['name'],
            'remaining': remaining,
            'percent': int(min(count_country, next_locked['threshold'])
                            / next_locked['threshold'] * 100),
        }
    return {'ladder': ladder, 'current': current, 'next': next_info}


@login_required
def statistics(request):
    count_country = visited_countries_count(request.user.id)
    month_trips = Tickets.objects.filter(
        user_id=request.user.id,
        date_start__month=date.today().month,
        date_start__year=date.today().year,
    )
    sum_price_month = sum(int(i['price']) for i in month_trips.values('price'))
    upcoming = Tickets.objects.filter(user_id=request.user.id, date_start__gte=date.today())
    trips_count = upcoming.count()
    context = {
        'count_country': count_country,
        'sum_price_month': sum_price_month,
        'later_trips': [],
        'trips_count': trips_count,
    }
    for content in upcoming:
        context['later_trips'].append({
            'trip_to': content.country,
            'trip_late': (content.date_end - content.date_start).days,
            'trip_plan': content.trip_plan,
        })
    return render(request, 'statistics.html', context=context)


@login_required
def profile(request):
    count_country = visited_countries_count(request.user.id)
    total_trips = Tickets.objects.filter(user_id=request.user.id).count()
    upcoming_count = Tickets.objects.filter(
        user_id=request.user.id, date_start__gte=date.today()).count()
    context = {
        'profile_user': request.user,
        'count_country': count_country,
        'total_trips': total_trips,
        'upcoming_count': upcoming_count,
        'achievements': build_achievements(count_country),
    }
    return render(request, 'profile.html', context=context)
