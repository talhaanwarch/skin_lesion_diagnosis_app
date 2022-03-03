from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    # path('upload',views.uploadImage, name='uploadImage'),
    #path('upoadbyURL',views.uploadURL, name='uploadURL')
    ]