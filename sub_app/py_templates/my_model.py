import os
import torch
from torchvision import transforms
from PIL import Image
import numpy as np 

model_densenet=os.path.join(os.path.dirname(os.path.dirname(__file__)),
	'py_templates/skin_model_densenet.pth')

model_efficient=os.path.join(os.path.dirname(os.path.dirname(__file__)),
	'py_templates/skin_model_final.pth')

image_path=os.path.dirname(os.path.dirname(__file__))

aug=transforms.Compose([
                        transforms.Resize((224,224)),
                        #transforms.CenterCrop(10),
                        transforms.RandomAffine(degrees=0, translate=None, scale=(1,1.5), shear=None, resample=Image.NEAREST, fillcolor=0),
                        transforms.RandomHorizontalFlip(),transforms.RandomVerticalFlip(),transforms.RandomRotation(360),
                        transforms.ToTensor(),
                        transforms.Normalize([0.5820, 0.4512, 0.4023], [0.2217, 0.1858, 0.1705]),

                        ])

#load model
model_d=torch.load(model_densenet, map_location=lambda storage, loc: storage)
model_e=torch.load(model_efficient, map_location=lambda storage, loc: storage)

#create a function that predict labels
def image_pred(url):
	try:
		new_url=image_path+url
	except TypeError:
		new_url=url
	img = Image.open(new_url)
	img=img.convert(mode='RGB')
	image = aug(img)
	image=image.unsqueeze(0) #add another dimension at 0
	out=torch.zeros((3,6))
	model_d.eval()
	model_e.eval()

	outd=model_d(image)
	oute=model_e(image)


	oute=torch.mean(oute,dim=0)
	outd=torch.mean(outd,dim=0)

	out=torch.stack((outd,oute),dim=0)

	out=torch.mean(out,dim=0)
	out=out.detach().numpy()
	out=np.argmax(out)
	return out






