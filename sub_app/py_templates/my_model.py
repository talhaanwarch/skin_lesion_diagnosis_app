import os
import torch
from torchvision import transforms
from PIL import Image
import numpy as np 

model_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),
	'py_templates/skin_model_b3.pth')
image_path=os.path.dirname(os.path.dirname(__file__))

aug=transforms.Compose([
                        transforms.Resize((300,300)),
                        #transforms.CenterCrop(10),
                        transforms.RandomAffine(degrees=0, translate=None, scale=(1,1.5), shear=None, resample=Image.NEAREST, fillcolor=0),
                        transforms.RandomHorizontalFlip(),transforms.RandomVerticalFlip(),transforms.RandomRotation(360),
                        transforms.ToTensor(),
                        transforms.Normalize([0.5820, 0.4512, 0.4023], [0.2217, 0.1858, 0.1705]),

                        ])

#load model
model=torch.load(model_path, map_location=lambda storage, loc: storage)

#create a function that predict labels
def image_pred(url):
	new_url=image_path+url
	img = Image.open(new_url)
	img=img.convert(mode='RGB')
	image = aug(img)
	image=image.unsqueeze(0) #add another dimension at 0
	out=torch.zeros((3,6))
	for i in range(3):
		out[i,:]=model(image)
	out=torch.mean(out,dim=0)
	print(out)
	out=out.detach().numpy()
	out=np.argmax(out)
	return out






