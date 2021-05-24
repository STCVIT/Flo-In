from django.shortcuts import render

from django.http.response import StreamingHttpResponse
from django.http import JsonResponse
from faceregister.collect_training_data import collectTrainingData
from django.contrib.auth.decorators import login_required
from faceregister.classifier import train_classifier
from django.http import HttpResponse
from django.template import loader, Context


def index(request):
	return render(request, 'home.html')

@login_required
def savefacedata(request):
    if request.method == 'GET':
        return render(request, 'savefacedata.html', {'form': FaceDataForm()})
    else:
        try:
            form = FaceDataForm(request.POST,request.Files)
            newfacedata = form.save(commit=False)
            newfacedata.user = request.user
            newfacedata.save()
            return redirect('home')
        except:
            return render(request, 'savefacedata.html', {'form': FaceDataForm(), 'error': 'Wrong data put in. Try Again'})


