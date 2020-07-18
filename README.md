# skin_lesion_diagnosis_app

# Create Django basic template

**Create virtual environmnet**  

python -m venv venv  
cd venv  
cd Scripts  
activate  
cd ..  
cd ..  
**Install django**  
pip install django  
**Create app**  
django-admin startproject main_app  
**Run Server**    
cd main_app  
python manage.py runserver  
**migrations**  
python manage.py migrate  
**create admin user**  
python manage.py createsuperuser  
**Now create first app**  
python manage.py startapp sub_app  

**Register this sub_app to main_app**  
Go to settings of main_app and in INSTALLED_APPS ass sub_app as follows  
```  
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sub_app',
]
```
**create urls**  
create urls.py inside sub_app  
attach urls.py of subapp to urls.py of main app, write following code in main app urls.py  
go to main_app url.py  
``` 
from django.contrib import admin
from django.urls import path,include
from sub_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('sub_app.urls'))
]
```

now go to urls.py of sub_app and add following  
```
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home')
    ]
```
**create a template**  
create a folder templates inside sub_app and inside the templates folder create home.html  
and write {{ print }}

connect this template folder with main_app
go to settings.py and after `STATIC_URL = '/static/'` add following  
`STATIC_ROOT = os.path.join(BASE_DIR, 'static')`



**Go to view.py of sub_app**
```
from django.shortcuts import render
def home(request):
	return render(request,'home.html',{'print':"every thing ok"})
```
**RUN app**  
Now run `python manage.py runserver` and you will every thing ok on browser  
**ERROR**  
if you got error  
TemplateDoesNotExist at / home.html in my project  
go to settings.py if main_app, in template section   
after 'DIRS':[], replace `[]` with `[os.path.join(BASE_DIR, 'templates'), ],`  
refresh the browser

# Add image fild to the basic template
**create a forum at front page (home) that can load an image**
```
<form action='upload' method="post" enctype="multipart/form-data">
	{% csrf_token %}
	<input type="file" name="image">
	<input type="submit" value="upload file">
</form>
```
**create a model on backend that can recive the image from front end**
```
from django.db import models
class image_classification(models.Model):
	pic=models.ImageField(upload_to='images')
```

**need pillow library for uploading image**  
pip install Pillow   

**run migration**  
python manage.py makemigrations  
python manage.py migrate  


**handle uploaded image**  
create a function in views.py of sub_app that can handle the image uploaded
```
from django.shortcuts import render
from .models import image_classification
from django.http import HttpResponseRedirect

# this home function is same as before
def home(request):
	return render(request,'home.html',{'print':"every thing ok"})

def uploadImage(request):
	print('image handling')
	img=request.FILES['image']
	image=image_classification(pic=img)
	image.save()
	return HttpResponseRedirect('/')
	#return render(request,'home.html')
```
**add image folder to settings**  
the image was saved in folder `images`, connect this folder with the system. Go to settings.py of main_app
above static lines add following  
MEDIA_ROOT = os.path.join(BASE_DIR, 'sub_app/media/') 
MEDIA_URL = '/media/'

**connect this with url.py of main_app**  
```
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('sub_app.urls'))
    ]

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```
**display the image**  
go to view.py of sub_app and change home function as follow  
```
def home(request):
	print('here u go')
	images=image_classification.objects.all()
	url=images[len(images)-1].pic.url
	return render(request,'home.html',{'print':"every thing ok",'url':url})
```
display image to `home.html` by adding this line 
`
<img src="{{url}}" ,width="500" height="400">`

# run the model
* run the ipynb file in colab gpu and save the model
* install pytorch cpu model, becuase heroku dont support gpu
`pip install torch==1.5.1+cpu torchvision==0.6.1+cpu -f https://download.pytorch.org/whl/torch_stable.html`
* install efficient net 
	pip install efficientnet_pytorch  
	 
* create py_templates folder in sub_app
* -create a file in my_model.py in py_templates
* save the model file in py_templates folder
* add path where the model file is hosted 
in my case, it is in py_template folder, so i add
```
model_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),
	'sub_app/py_templates/skin_model.pth')
```
* create a function that predict image output
the path of image in this function should be  
`image_path=os.path.dirname(os.path.dirname(__file__))+url` where url is argument of the function

* import this function in views.py file

# host the app to herko
* create an account on heroku and github
* upload all of your files at github, dont upload venv folder
* allowed host  
in settings of main_app, change `ALLOWED_HOSTS = []` to `ALLOWED_HOSTS = ['*']`  
* create Procfile  
`web: gunicorn main_app.wsgi:application --log-file -`
* install gunicorn  
pip install gunicorn  
* create a requirement files
`pip freeze > requirements.txt`
* creat a runtime.txt file comprises of your python version.   
check using python --version and add it as python-3.7.6   
you can have different version , i have 3.7.6  

* replace these two line in requirements.txt
```
torch==1.5.1+cpu
torchvision==0.6.1+cpu
```
with these  
```
https://download.pytorch.org/whl/cpu/torch-1.1.0-cp37-cp37m-linux_x86_64.whl  
https://download.pytorch.org/whl/cpu/torchvision-0.3.0-cp37-cp37m-linux_x86_64.whl  
```
* for static files at heroku, follow this   
https://devcenter.heroku.com/articles/django-assets  

* set DEBUG =False in settings.py
* Go to app settings and at heroku Config Vars save secret keys with out ''
such as 
SECRET_KEY = abcow@h!n8-abc*)abc1xx6)hok_zc@pro$s)6%0abc@u9cztm  
create .env file in main_app and save secret key as   
SECRET_KEY = '4dxow@h!n8-thd*)mpw1xx6)hok_zc@pro$s)6%0blb@u9cztm'  
install pip install django-environ and save it to requirement.txt   
add .env to gitignore   



# Updates  
https://stackoverflow.com/a/49374520/11170350
