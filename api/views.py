import os

from .renderers import ImageRenderer
from .serializers import userDataSerializer
from .permissions import IsOwnerProfileOrReadOnly
from accounts.models import UserData
from accounts.recognise2 import authenticate_user
from rest_framework import status
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

k = dict()
# Create your views here.

ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', 
                            '.JPG', '.JPEG', '.PNG']

class ImageAPIView(APIView):
    renderer_classes = [ImageRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return JsonResponse({'get request':'ok'})

    def post(self, request, *args, **kwargs):
        if 'image' in request.FILES:
            file = request.FILES['image']
            base, ext = os.path.splitext(file.name)
            if not ext in ALLOWED_IMAGE_EXTENSIONS:
                return JsonResponse({'error': 'Invalid image file format.'}, status=400)
            default_storage.save(str(request.user.id)+".png",file)
            k[request.user.id] = authenticate_user(str(request.user.id), os.path.join(settings.BASE_DIR,"media",str(request.user.id)+".png"))
            print(k)
            return JsonResponse({"match" : k[request.user.id]})
        else:
            return JsonResponse({'error': 'No file found.'}, status=400)

@permission_classes([AllowAny])
@api_view(['POST'])
def LogoutAndBlacklistRefreshTokenForUserView(request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dataList(request):
    datas = UserData.objects.filter(user=request.user)
    serializer = userDataSerializer(datas, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def dataDetail(request, url):
    datas = UserData.objects.filter(url=url, user=request.user).first()
    serializer = userDataSerializer(datas, many = False)
    return Response(serializer.data)

@api_view(['POST'])
def dataCreate(request):
    data={
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'url': request.data.get('url'),
            'user': request.user.id
            }
    try:
        udata = UserData.objects.filter(url = request.data.get('url'), user=request.user).first()
        serializer = userDataSerializer(instance=udata, data=data)
    except:
        serializer = userDataSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def dataUpdate(request, url):
    data = UserData.objects.get(url = url)
    serializer = userDataSerializer(instance=data, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def dataDelete(request, url):
    task = UserData.objects.get(url = url)
    task.delete()
    return Response("Taks deleted successfully.")