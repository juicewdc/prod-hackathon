from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework import status
from .forms import ProjectUserRegisterForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def main(request):
    if request.user.is_authenticated:
        return redirect('mainapp:main')
    context = {
        'auth': request.user.is_authenticated
    }
    return render(request, template_name='first_page.html', context=context)


@swagger_auto_schema(
    method='get',
    operation_description="Получить данные с параметрами",
    manual_parameters=[
        openapi.Parameter('param', openapi.IN_QUERY, description="Пример параметра", type=openapi.TYPE_STRING)
    ],
    responses={200: openapi.Response('Success')},
)
@api_view(['GET'])
def is_authenticated(request):
    return Response({'is_authenticated': request.user.is_authenticated})

def authentication(request):
    context = {
        'auth': request.user.is_authenticated
    }
    return render(request, template_name='auth.html', context=context)


def register(request):
    context = {
        'auth': request.user.is_authenticated
    }
    return render(request, template_name='register.html', context=context)

@swagger_auto_schema(
    method='post',
    operation_description="Получить данные с параметрами",
    manual_parameters=[
        openapi.Parameter('param', openapi.IN_QUERY, description="Пример параметра", type=openapi.TYPE_STRING)
    ],
    responses={200: openapi.Response('Success')},
)
@api_view(['POST'])
def request_register(request):
    if request.method == 'POST':
        try:
            form = ProjectUserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.save()
            else:
                context = {
                    'error': form.errors
                }
                return Response(context)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            context = {
                'auth': request.user.is_authenticated,
                'error': 'Ошибка регистрации, попробуйте снова.'
            }
            return Response(context)

def register_process(request):
    if request.method == 'POST':
        try:
            form = ProjectUserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.save()
            else:
                context = {
                    'error': form.errors
                }
                return render(request, template_name='register.html', context=context)
            return redirect('firstapp:authenticate')
        except Exception as e:
            context = {
                'auth': request.user.is_authenticated,
                'error': 'Ошибка регистрации, попробуйте снова.'
            }
            return render(request, template_name='register.html', context=context)

@swagger_auto_schema(
    method='post',
    operation_description="Получить данные с параметрами",
    manual_parameters=[
        openapi.Parameter('param', openapi.IN_QUERY, description="Пример параметра", type=openapi.TYPE_STRING)
    ],
    responses={200: openapi.Response('Success')},
)
@api_view(['POST'])
def request_authenticate(request):
    if request.method == 'POST':
        login_user = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=login_user, password=password)
        if user:
            login(request, user)
            return Response({'status': 200})
        return redirect({'status': 400})

def authentication_process(request):
    if request.method == 'POST':
        login_user = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=login_user, password=password)
        if user:
            login(request, user)
            return redirect('mainapp:main')
        return redirect('firstapp:authenticate')



def user_logout(request):
    logout(request)
    return redirect('firstapp:authenticate')