import os

# Imports from other modules
from .renderers import ImageRenderer
from .serializers import userDataSerializer
from .permissions import IsOwnerProfileOrReadOnly
from accounts.models import UserData, FaceData
from accounts.encoding import encoding_recognise

# Imports from installed modules
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
from cryptography.fernet import Fernet
import random

# defined Encryption key
k = dict()
key = b"0Bnw3EFq0OSgfKA26qxJBkmWC9kABY1Xdfw8Ng1DHss="
fernet = Fernet(key)


def sendFernet():
    """Generate a random key and encrypt it with Fernet"""
    return fernet


ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]


class ImageAPIView(APIView):
    renderer_classes = [ImageRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return JsonResponse({"get request": "ok"})

    def post(self, request, *args, **kwargs):
        if "image" in request.FILES:
            file = request.FILES["image"]
            base, ext = os.path.splitext(file.name)
            if not ext in ALLOWED_IMAGE_EXTENSIONS:
                return JsonResponse({"error": "Invalid image file format."}, status=400)
            url = str(request.user.id) + str(random.randint(0, 5000))
            default_storage.save(url + ".png", file)
            fd = FaceData.objects.get(user=request.user)
            k[request.user.id] = encoding_recognise(
                str(request.user.id),
                os.path.join(settings.BASE_DIR, "media", url + ".png"),
            )
            print(k)
            return JsonResponse({"match": k[request.user.id]})
        else:
            return JsonResponse({"error": "No file found."}, status=400)


@permission_classes([AllowAny])
@api_view(["POST"])
def LogoutAndBlacklistRefreshTokenForUserView(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def dataList(request):
    datas = UserData.objects.filter(user=request.user)
    serializer = userDataSerializer(datas, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def dataDetail(request, url):
    print(url)
    print(request.user)

    datas = UserData.objects.filter(url=url, user=request.user).first()
    print(datas)
    print(datas.password)
    serializer = userDataSerializer(datas, many=False)
    password = fernet.decrypt(
        bytes(serializer.data["password"], encoding="utf8")
    ).decode()
    print(password)
    resp = serializer.data
    resp["password"] = password
    print(resp)
    return Response(resp)


@api_view(["POST"])
def dataCreate(request):
    password = request.data.get("password")
    password = fernet.encrypt(password.encode())
    password = password.decode("utf8")
    data = {
        "username": request.data.get("username"),
        "password": password,
        "url": request.data.get("url"),
        "user": request.user.id,
    }
    print(data)
    try:
        udata = UserData.objects.filter(
            url=request.data.get("url"), user=request.user
        ).first()
        serializer = userDataSerializer(instance=udata, data=data)
    except:
        serializer = userDataSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
def dataUpdate(request, url):
    data = UserData.objects.get(url=url)
    serializer = userDataSerializer(instance=data, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def dataDelete(request, url):
    data = UserData.objects.get(url=url)
    data.delete()
    return Response("Password deleted successfully.")


@api_view(["POST"])
def checkPattern(request):
    data = FaceData.objects.get(user=request.user)
    pinData = request.data
    if data.pin == pinData["pin"]:
        print("Matched")
        return JsonResponse({"PIN": "Matched"})
    else:
        return JsonResponse({"PIN": "Unmatched"})
