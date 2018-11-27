from django.shortcuts import render
from datetime import datetime, date
from .models import *

def root(request):
    today = date.today()
    progressium = Progressium(Habit.objects.all())
    return render(request, "home.html", {
     "progressium": progressium
    })
