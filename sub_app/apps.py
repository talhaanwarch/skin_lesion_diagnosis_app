from django.apps import AppConfig
import os
from django.conf import settings
import onnxruntime
class SubAppConfig(AppConfig):
	name = 'sub_app'
	model1_path = os.path.join(settings.MODELS, 'efficientnet_b1_pruned_skin.onnx')
	model2_path =os.path.join(settings.MODELS, 'mixnet_l_skin.onnx')
	model3_path =os.path.join(settings.MODELS, 'mobilenetv3_rw_skin.onnx')

	model1_session = onnxruntime.InferenceSession(model1_path)
	model2_session = onnxruntime.InferenceSession(model2_path)
	model3_session = onnxruntime.InferenceSession(model3_path)
