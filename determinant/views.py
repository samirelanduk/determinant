from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime, date, timedelta
from .models import *
from .forms import *

def root(request):
    selected = None
    if request.method == "POST":
        habit = list(Habit.objects.all())[int(request.POST["habit"])]
        day = datetime.strptime(request.POST["day"], "%Y-%m-%d").date()
        record = habit.record_set.filter(date=day)
        if record:
            record = record.first()
            record.success = not record.success
            record.save()
        else:
            Record.objects.create(
             habit=habit, date=day, success=habit.positive
            )
        messages.add_message(request, messages.INFO, day)
        messages.add_message(request, messages.INFO, int(request.POST["habit"]))
        return redirect(request.get_full_path())
    today = datetime.strptime(request.GET["day"], "%Y-%m-%d").date()\
     if "day" in request.GET else date.today()
    progressium = Progressium(Habit.objects.all(), end=today)
    m = []
    for message in messages.get_messages(request):
        try:
            m.append(int(message.message))
        except: m.append(message.message)
    return render(request, "home.html", {
     "progressium": progressium,
     "previous": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
     "next": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
     "messages": m
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
