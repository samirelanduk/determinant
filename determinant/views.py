from django.shortcuts import render
from datetime import datetime, date
from .models import *

def root(request):
    today = datetime.strptime(request.GET["day"], "%Y-%m-%d").date() if "day" in request.GET else date.today()
    progressium = Progressium(Habit.objects.all(), end=today)
    return render(request, "home.html", {
     "progressium": progressium
    })
