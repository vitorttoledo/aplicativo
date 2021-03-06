# coding: utf-8
import json
from django.http.response import HttpResponse, JsonResponse
from django.contrib import auth
from commons.django_model_utils import get_or_none
from commons.django_views_utils import ajax_login_required
from core.service import log_svc, globalsettings_svc, jogos_svc
from django.views.decorators.csrf import csrf_exempt


def dapau(request):
    raise Exception('break on purpose')


@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    user_dict = None
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            log_svc.log_login(request.user)
            user_dict = _user2dict(user)
    return JsonResponse(user_dict, safe=False)


def logout(request):
    if request.method.lower() != 'post':
        raise Exception('Logout only via post')
    if request.user.is_authenticated:
        log_svc.log_logout(request.user)
    auth.logout(request)
    return HttpResponse('{}', content_type='application/json')


def whoami(request):
    i_am = {
        'user': _user2dict(request.user),
        'authenticated': True,
    } if request.user.is_authenticated else {'authenticated': False}
    return JsonResponse(i_am)


def settings(request):
    le_settings = globalsettings_svc.list_settings()
    return JsonResponse(le_settings)

def list_for_user(request):
    lista = list(jogos_svc.list_for_user())
    jogos = []
    for i in lista:
        jogos.append(i.to_dict_json())
    return JsonResponse(jogos, safe=False)

def list_jogos(request):
    return JsonResponse(jogos_svc.list_jogos_by_esporte(), safe=False)

def create_jogo(request):
    criador = request.POST['criador']
    esporte = request.POST['esporte']
    dia = request.POST['dia']
    horas = request.POST['horas']
    descricao = request.POST['descricao']
    imagem = request.POST['imagem']
    participantes = request.POST['participantes']
    jogo = jogos_svc.create_jogo(
        criador=criador, esporte=esporte, dia=dia, horas=horas, descricao=descricao, imagem=imagem, participantes=participantes)
    return JsonResponse(jogo, safe=False)

def search_info(request, info):
    result = jogos_svc.search_info(info)
    return JsonResponse(result, safe=False)

def participate(request, username, jogo):
    result = jogos_svc.participate(username, jogo)
    return JsonResponse(result, safe=False)

def unparticipate(request, username, jogo):
    result = jogos_svc.unparticipate(username, jogo)
    return JsonResponse(result, safe=False)

def _user2dict(user):
    d = {
        'id': user.id,
        'name': user.get_full_name(),
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'permissions': {
            'ADMIN': user.is_superuser,
            'STAFF': user.is_staff,
        }
    }
    return d
