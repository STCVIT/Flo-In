from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from django.http import JsonResponse
from faceregister.collect_training_data import VideoCamera
from faceregister.classifier import train_classifier
from django.http import HttpResponse
from django.template import loader, Context

camera = VideoCamera()

def index(request):
	return render(request, 'home.html')


def gen():
	global camera
	id=0
	while id<100:
		frame, check = camera.get_frame(id)
		if check:
			id+=1
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	train_classifier("swarukharul")



def video_feed(request):
	return StreamingHttpResponse(gen(),
					content_type='multipart/x-mixed-replace; boundary=frame')