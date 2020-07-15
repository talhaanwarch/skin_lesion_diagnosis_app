from django.db import models

from django.db import models
class image_classification(models.Model):
	pic=models.ImageField(upload_to='images')