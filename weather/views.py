from django.shortcuts import render,redirect
from .models import City
import requests
from .forms import AddCityForm
from django.contrib import messages

def home(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=fb6ac297da1932a02ac6d41a1ce50853'
	weather_data = []

	for city in City.objects.all():
		r = requests.get(url.format(city.city_name)).json()
		weather_data_single = {
			"city":city.city_name,
			"temprature": r["main"]["temp"],
			"description": r["weather"][0]["description"],
			"icon":  r["weather"][0]["icon"]
		}
		weather_data.append(weather_data_single)

	if request.method == "POST":
		form = AddCityForm(request.POST)
		if form.is_valid():
			new_city = form.cleaned_data.get("city_name")
			if City.objects.filter(city_name = new_city).count() == 0:
				r = requests.get(url.format(new_city)).json()
				if r['cod'] == 200:
					form.save()
					messages.success(request,f'{new_city} has been added to the list!')
					return redirect("home")
				else:
					messages.warning(request, f'{new_city} does not exist in the world!')
					return redirect("home")
			else:
				messages.warning(request, "City already exists in the Database!")
				return redirect("home")

	else: 
		form = AddCityForm()

	context = {"weather_data": weather_data, "form":form}
	return render(request, "weather/home.html", context)

def delete(request, city_name):
	city = City.objects.get(city_name = city_name)
	city.delete()
	return redirect("home")