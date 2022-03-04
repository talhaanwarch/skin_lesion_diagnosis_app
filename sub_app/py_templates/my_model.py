import os
from PIL import Image
import numpy as np 
from ..apps import SubAppConfig



image_path=os.path.dirname(os.path.dirname(__file__))


#load model

def getpred(ort_session,img):
	ort_inputs = {ort_session.get_inputs()[0].name: img}
	ort_outs = ort_session.run(None, ort_inputs)[0]
	#img_out_y = np.argmax(ort_outs[0],1)[0]
	return ort_outs.ravel()

#create a function that predict labels
def image_pred(url,upload=True):
	if upload:
		new_url=image_path+url
	else:
		new_url=url
	img = Image.open(new_url)
	img=img.convert(mode='RGB')
	img=img.resize((224,224))
	img=np.array(img)/255
	image = (img - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
	print('image.shape',image.shape)#(224, 224, 3)
	img=np.moveaxis(image,2,0)#(3,224, 224)
	img=np.expand_dims(img,0)#(1,3,224, 224)
	img=img.astype(np.float32)#ort require float instead of double

	sess1=SubAppConfig.model1_session
	out1=getpred(sess1,img)
	out11=getpred(sess1,np.flip(img,0))
	out12=getpred(sess1,np.flip(img,1))

	sess2=SubAppConfig.model2_session
	out2=getpred(sess2,img)
	out21=getpred(sess2,np.flip(img,0))
	out22=getpred(sess2,np.flip(img,1))

	sess3=SubAppConfig.model3_session
	out3=getpred(sess3,img)
	out31=getpred(sess3,np.flip(img,0))
	out32=getpred(sess3,np.flip(img,1))

	# out1=np.mean([out1,out11,out12],axis=0)
	# out2=np.mean([out2,out21,out22],axis=0)
	# out3=np.mean([out3,out31,out32],axis=0)

	
	print(np.argmax(out1),np.argmax(out2),np.argmax(out3))
	out=np.mean([out1,out2,out3],axis=0)

	prob=np.exp(out)/sum(np.exp(out))

	return np.argmax(out),prob.round(3)






