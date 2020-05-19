from django.http import HttpResponse
from django.shortcuts import render, redirect
from multiprocessing import Process
from .functions import *


def home(request):
	if request.method == 'POST':
		file = None
		try:
			file=request.FILES['File']
			handle_uploaded_file(file)
		except:
			pass
		name=request.POST["Name"]
		email=request.POST["Email"]
		sequence = request.POST["Sequence"]
		if(not file and not sequence):
			return render(request, "home.html", {'error': 'Please provide a sequence'})
		background_thread=Process(target=run_task, args=(file, name, email))
		background_thread.daemon=True
		background_thread.start()
		return redirect("submitted")
	else:
		return render(request,"home.html")


def submitted(request):
	return render(request, "submitted.html")