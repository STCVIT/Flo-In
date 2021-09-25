import os
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage, FileSystemStorage

# Local imports
from api.views import sendFernet
from .encoding import encoding_recognise
from .models import MyUser, UserData, FaceData
from .collect_training_data import collectTrainingData
from .Forms import UserAdminCreationForm, AuthenticationForm, UserDataForm, FaceDataForm

k = dict()


def home(request):
    return render(request, "home.html")


@login_required
def profile(request):
    datas = UserData.objects.filter(user=request.user)
    fernet = sendFernet()
    for data in datas:
        data.password = fernet.decrypt(bytes(data.password, encoding="utf8")).decode()
        print(data.password)
    return render(request, "profile.html", {"datas": datas})


def loginuser(request):
    """Login user"""
    if request.method == "GET":
        return render(request, "loginuser.html", {"form": AuthenticationForm()})
    else:
        try:
            user = authenticate(
                request, email=request.POST["email"], password=request.POST["password"]
            )
            if user is None:
                return render(
                    request,
                    "loginuser.html",
                    {
                        "form": AuthenticationForm(),
                        "error": "User password did not match",
                    },
                )
            else:
                login(request, user)
                return redirect("profile")
        except:
            # Create a new user
            if request.POST["password1"] == request.POST["password2"]:
                try:
                    user = MyUser.objects.create_user(
                        password=request.POST["password1"], email=request.POST["email"]
                    )
                    user.save()
                    login(request, user)
                    return redirect("profile")
                except IntegrityError:
                    return render(
                        request,
                        "loginuser.html",
                        {
                            "error": "This email id has already been registered. Please try to login or use different email id"
                        },
                    )
                except ValueError:
                    return render(
                        request, "loginuser.html", {"error": "Please enter valid email"}
                    )
            else:
                # tell the user the password didn't match
                return render(
                    request, "loginuser.html", {"error": "Passwords did not match"}
                )


@login_required
def logoutuser(request):
    """Logout user"""
    if request.method == "POST":
        logout(request)
        return redirect("home")


@login_required
def savedata(request):
    """Save user data"""
    if request.method == "GET":
        return render(request, "savedata.html", {"form": UserDataForm()})
    else:
        try:
            form = UserDataForm(request.POST)
            newdata = form.save(commit=False)
            newdata.user = request.user
            newdata.save()
            return redirect("profile")
        except:
            return render(
                request,
                "savedata.html",
                {"form": UserDataForm(), "error": "Wrong data put in. Try Again"},
            )


# Register face
@login_required
def savefacedata(request):
    """Save face data"""
    if request.method == "GET":
        return render(request, "savefacedata.html", {"form": FaceDataForm()})
    else:
        try:
            fd = get_object_or_404(FaceData, user=request.user)
            form = FaceDataForm(request.POST, request.FILES, instance=fd)
            form.save()
        except:
            form = FaceDataForm(request.POST, request.FILES)
            newfacedata = form.save(commit=False)
            newfacedata.user = request.user
            newfacedata.save()
        resp = collectTrainingData(str(request.user.id))
        if not resp["Success"]:
            fd = FaceData.objects.get(user=request.user)
            fd.save()
        return JsonResponse(resp)


@login_required
def checkfacedata(request):
    """Check Face Recognition model"""
    if request.method == "GET":
        return render(request, "checkfacedata.html", {"form": FaceDataForm()})
    else:
        checkImage = request.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(checkImage.name, checkImage)
        filename = os.path.join(settings.BASE_DIR, "media", filename)
        fd = FaceData.objects.get(user=request.user)
        k[request.user.id] = encoding_recognise(str(request.user.id), filename)
        print(k)
        return JsonResponse(k[request.user.id])


@login_required
def setpattern(request):
    """Set PIN for alternate authentication"""
    fd = FaceData.objects.get(user=request.user)
    print(fd)
    fd.pin = request.POST["password"]
    print(fd.pin)
    fd.save()
    return redirect("savefacedata")
