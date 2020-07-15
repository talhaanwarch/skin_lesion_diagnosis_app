from django.shortcuts import render
from .models import image_classification
from django.http import HttpResponseRedirect
from .py_templates.my_model import image_pred

def home(request):
	print('here u go')
	images=image_classification.objects.all()
	url=images[len(images)-1].pic.url
	out=image_pred(url)
	out={0:'BCC',1:'ACK',2:'NEV',3:'SEK',4:'SCC',5:'MEL'}[int(out)]
	return render(request,'home.html',{'pred':out,'url':url})
def uploadImage(request):
	print('image handling')
	img=request.FILES['image']
	image=image_classification(pic=img)
	image.save()
	return HttpResponseRedirect('/')
	#return render(request,'home.html')
