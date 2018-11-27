from django.db import models
from datetime import datetime, date, timedelta

class Habit(models.Model):

    name = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateField()
    reward = models.CharField(max_length=16)
    penalty = models.IntegerField()
    cheat = models.CharField(max_length=32)

    class Meta:
        ordering = ["start_date"]


    def history(self):
        return History(self)


    def cheats(self):
        numbers = [int(num) for num in self.cheat.split(",")]
        cheats = [numbers.pop(0)]
        while numbers:
            if numbers[0] > cheats[-1]:
                cheats.append(cheats[-1] + 1)
            else:
                cheats.append(cheats[-1] - 1)
            if cheats[-1] == numbers[0]: numbers.pop(0)
        return cheats



class Record(models.Model):

     habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
     date = models.DateField()
     success = models.BooleanField()

     class Meta:
         ordering = ["date"]



class Progressium:
    """A representation of a user's habit history over all their habits."""

    def __init__(self, habit_set):
        self.habits = habit_set
        start = self.habits.first().start_date
        today = date.today()
        day = start
        self.days = []
        histories = [habit.history() for habit in habit_set]
        running = 0
        while not self.days or self.days[-1].date != today:
            habit_days = []
            for history in histories:
                habit_days.append(history.get_day(day))
            self.days.append(Day(date=day, habit_days=habit_days, previous_running=running))
            running = self.days[-1].running_total
            day += timedelta(days=1)



class History:
    """A representation of a single habit's history."""

    def __init__(self, habit):
        self.habit = habit
        self.days = []
        today = date.today()
        day = habit.start_date
        cheats = habit.cheats()
        cheat = cheats[0]
        last_penalty = 0
        print(type(habit.penalty))
        while not self.days or self.days[-1].date != today:
            record = habit.record_set.filter(date=day)
            success = record.first().success if record else False
            cheat_allowed = cheat <= 0
            self.days.append(HabitDay(
             date=day, success=success,
             score=1 if success else (0 if cheat_allowed else (habit.penalty * (last_penalty - 1)))
            ))
            last_penalty = 0 if success or cheat_allowed else last_penalty - 1
            if not success and not cheat_allowed: cheat = cheats[0] + 1
            if cheat_allowed and not success:
                if len(cheats) > 1: cheats.pop(0)
                cheat = cheats[0]
            day += timedelta(days=1)
            cheat -= 1


    def get_day(self, date):
        for day in self.days:
            if day.date == date:
                return day
        return None



class HabitDay:
    """A day in a habit."""

    def __init__(self, date, success, score):
        self.date = date
        self.success = success
        self.score = score



class Day:
    """A day containing multiple habit efforts."""

    def __init__(self, date, habit_days, previous_running):
        self.date = date
        self.habit_days = habit_days
        self.running_total = previous_running + self.score_total()


    def scores(self):
        return [day.score if day else None for day in self.habit_days]


    def score_total(self):
        return sum([s for s in self.scores() if s is not None])
