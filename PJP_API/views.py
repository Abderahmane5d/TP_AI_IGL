from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

from django.db.models import Q

from rest_framework import status

from django.contrib.auth import authenticate, login

# from rest_framework.fields import CurrentUserDefault

# Create your views here.


@api_view(['POST'])
def userDetail(request):
    pk = request.data['owner']
    user = UserModel.objects.get(id=pk)
    serializer = UserModelSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def logIn(request):
    email = request.data['email']

    user = UserModel.objects.all().filter(email=email)

    if user:
        # utilisateur existe
        user = UserModel.objects.get(email=email)
        userData = UserModelSerializer(user)

        return Response(userData.data)
    else:
        # utilisateur n'existe pas
        response = {
            "email": "no user"
        }
        return Response(response)


@api_view(["POST"])
def signUp(request):

    serializer = UserModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'somthing': '/something/',
        'overview': '/'
    }
    return Response(api_urls)


@api_view(['POST'])
def messageList(request):
    messages = Message.objects.filter(destination=request.data['id'])
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def messageDetail(request, pk):
    message = Message.objects.get(id=pk)  # union
    serializer = MessageSerializer(message, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def messageCreate(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():

        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def messageUpdate(request, pk):
    message = Message.objects.get(id=pk)
    serializer = MessageSerializer(instance=message, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def messageDelete(request, pk):
    message = Message.objects.get(id=pk)
    message.delete()
    return Response("deleted successfully")

# AI API


@api_view(['GET'])  # ordre
def aiList(request):
    # user = CurrentUserDefault()
    print(request.user.id)
    # AIs = AI.objects.all().filter(owner=request.user.id).order_by('-id')
    AIs = AI.objects.all().order_by('-id').exclude(owner=request.user.id)
    serializer = AiSreializer(AIs, many=True)
    return Response(serializer.data)


@api_view(['POST'])  # ordre
def myAiList(request):
    # user = CurrentUserDefault()
    print(request.data['id'])
    AIs = AI.objects.all().filter(owner=request.data['id']).order_by('-id')
    serializer = AiSreializer(AIs, many=True)
    return Response(serializer.data)


@api_view(['GET'])  # ordre
def AiSignal(request):
    # user = CurrentUserDefault()
    print(request.user.id)
    AIs = AI.objects.all().filter(Signal=True).order_by('-id')
    print(AIs)
    serializer = AiSreializer(AIs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def aiDetail(request, pk):
    ai = AI.objects.get(id=pk)
    serializer = AiSreializer(ai, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def aiCreate(request):
    request.data['Signal'] = False

    serializer = AiSreializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def aiUpdate(request, pk):
    ai = AI.objects.get(id=pk)
    serializer = AiSreializer(instance=ai, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def aiDelete(request):
    ai = AI.objects.get(id=request.data['id'])
    ai.delete()
    return Response("deleted successfully")


@api_view(['GET'])  # ordre
def favorieList(request):
    # user = CurrentUserDefault()
    print(request.user)
    # favories = Favories.objects.all()
    favories = Favories.objects.all().filter(user=request.user.id).order_by('-id')
    serializer = FavoriesSerializer(favories, many=True)
    return Response(serializer.data)


@api_view(['GET'])  # ordre
def aiSearch(request):
    pk = request.query_params.get('kw')  # ************* all
    keys = pk.split('-')
    lookup = Q(titre__icontains=keys[0]) | Q(description__icontains=keys[0])
    print()
    print(lookup)
    print()
    AIs = AI.objects.all().filter(lookup)
    for k in keys:
        lookup = Q(titre__icontains=k) | Q(description__icontains=k)
        AIs = AIs.union(AI.objects.all().filter(lookup))
    serializer = AiSreializer(AIs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def aiSearchMixte(request):
    type = request.query_params.get('type')
    wilaya = request.query_params.get('wilaya')
    commune = request.query_params.get('commune')
    date_debut = request.query_params.get('date_debut')
    date_fin = request.query_params.get('date_fin')
    ai = AI.objects.all()
    if type != "*":
        ai = ai.filter(type=type)
    print(ai)
    if wilaya != "*" and commune != "*":
        lookup = Q(Location__wilaya__contains=wilaya) and Q(
            Location__commune__contains=commune)
        ai = ai.filter(lookup)
    elif wilaya != "*" and commune == "*":

        locations = Location.objects.filter(wilaya=wilaya).values()
        print
        print(locations)
        print
        ai_loc = AI.objects.filter(location=locations[0]['id'])
        for loc in locations:
            ai_loc.union(AI.objects.filter(location=loc['id']))
        # lookup = Q(Location__wilaya__exact=wilaya)
        ai = ai.intersection(ai_loc)
        # ai=ai.filter(lookup)
        # locations = Location.objects.filter(wilaya=wilaya).values()
        # ai_loc = AI.objects.filter(location=locations[0]['id'])
        # ai=ai.intersection(ai_loc)
    elif wilaya == "*" and commune != "*":
        locations = Location.objects.filter(commune=commune).values()
        print
        print(locations)
        print
        ai_loc = AI.objects.filter(location=locations[0]['id'])
        for loc in locations:
            ai_loc.union(AI.objects.filter(location=loc['id']))
        # lookup = Q(Location__wilaya__exact=wilaya)
        ai = ai.intersection(ai_loc)
    if date_debut != '*' and date_fin != '*':
        ai = ai.filter(Q(created__range=[date_debut, date_fin]))
    serializer = AiSreializer(ai, many=True)
    return Response(serializer.data)
