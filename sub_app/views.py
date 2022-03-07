from django.shortcuts import render
from django.http import HttpResponseRedirect
from .py_templates.my_model import image_pred
from PIL import Image
import requests
import numpy as np
from .forms import SkinForm
from django.core.files.storage import FileSystemStorage
import os 
from django.conf import settings
decode={0: 'Nevus (NEV)', 1: 'Basal Cell Carcinoma (BCC)', 2: 'Actinic Keratosis (ACK)',
 3: 'Squamous Cell Carcinoma (SCC)', 4: 'Melanoma', 5: 'Benign Keratosis lesions (BKL)'}


def home(request):
	
	if request.method=='POST':
		form = SkinForm(request.POST,request.FILES)
		if form.is_valid():
			print('form is valid')
			img=form.cleaned_data['pic']
			url=form.cleaned_data['url']
			if img:
				fs = FileSystemStorage()
				filename = fs.save(img.name.replace(' ',''), img)

				path = fs.url(filename)
				label,proba=image_pred(path)
				#path=os.path.join(settings.MEDIA_ROOT,filename)
				print('path',path)
			elif url:
				imgurl=requests.get(url, stream=True).raw
				label,proba=image_pred(imgurl,upload=False)
				path=url
			else:
				form = SkinForm()
				return render(request,'home.html',{'form':form,'pred':"None"})


			out=list(reversed(sorted(zip(list(proba*100), list(decode.values())))))
			out=[[j,np.round(i,3)] for i,j in out]

			statement='Chances of {} are {}%'.format(decode[label],int(proba[label]*100))
			return render(request,'home.html',{'form':form,'pred':out,'path':path,'disease':statement})
	else:
		form = SkinForm()
		return render(request,'home.html',{'form':form,'pred':"None"})



