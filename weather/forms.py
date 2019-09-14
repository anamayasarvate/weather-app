from django import forms
from .models import City 

class AddCityForm(forms.ModelForm):
	city_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class' : 'input', 'placeholder': 'City Name'}))
	
	class Meta():
		model = City
		fields = ["city_name"]
    





