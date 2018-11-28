from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, date, timedelta
from .models import *
from .forms import *

def root(request):
    today = datetime.strptime(request.GET["day"], "%Y-%m-%d").date() if "day" in request.GET else date.today()
    progressium = Progressium(Habit.objects.all(), end=today)
    return render(request, "home.html", {
     "progressium": progressium,
     "previous": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
     "next": (today + timedelta(days=1)).strftime("%Y-%m-%d")
    })


def habit(request, pk):
    habit = get_object_or_404(Habit, id=pk)
    form = HabitForm(instance=habit)
    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid:
            form.save()
            return redirect(request.path)
    return render(request, "habit.html", {
     "habit": habit,
     "form": HabitForm(instance=habit)
    })
