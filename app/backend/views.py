from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import status


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def hello(request):
    return HttpResponse("<h1>chuj</h1>")


def create_user(request):
    print(request.json())
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    if username is None or password is None or email is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username, email, password)
    user.save()

    return Response(status=status.HTTP_201_CREATED)




