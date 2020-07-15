# skin_lesion_diagnosis_app
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
from todo_list import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('todo_list.urls'))
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

**Go to view.py of sub_app**
```
from django.shortcuts import render
def home(request):
	return render(request,'home.html',{'print':"every thing ok"})
```
Now run python manage.py runserver and you will every thing ok on browser


