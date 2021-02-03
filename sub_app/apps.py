from django.apps import AppConfig
import os
from django.conf import settings
import torch
class SubAppConfig(AppConfig):
	name = 'sub_app'
	model_densenet=model_path = os.path.join(settings.MODELS, 'skin_model_densenet.pth')
	model_efficient=os.path.join(settings.MODELS, 'skin_model_final.pth')
	model_d=torch.load(model_densenet, map_location=lambda storage, loc: storage)
	model_e=torch.load(model_efficient, map_location=lambda storage, loc: storage)
