from django import forms
from .models import SkinModel

class SkinForm(forms.ModelForm):
	class Meta:
		model=SkinModel
		fields = "__all__"