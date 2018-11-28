from django.db import models
from datetime import timedelta

class Habit(models.Model):

    name = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateField()
    reward = models.CharField(max_length=16)
    penalty = models.IntegerField()
    cheat = models.CharField(max_length=32)
    positive = models.BooleanField()

    class Meta:
        ordering = ["start_date"]


    def history(self, day):
        return History(self, day)


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

    def __init__(self, habit_set, end):
        self.habits = habit_set
        start = self.habits.first().start_date
        today = end
        day = start
        self.days = []
        histories = [habit.history(end) for habit in habit_set]
        self.histories = histories
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

    def __init__(self, habit, today):
        self.habit = habit
        self.days = []
        day = habit.start_date
        cheats = habit.cheats()
        cheat = cheats[0]
        last_penalty = 0
        self.badges = 0
        print(today)
        while not self.days or self.days[-1].date != today:
            print(day)
            record = habit.record_set.filter(date=day)
            success = record.first().success if record else not habit.positive
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
            if cheat == 0: self.badges += 1
        self.next_cheat = today + timedelta(days=cheat + 1) if cheat > 0 else "Now"
        self.target_streak = cheats[0]


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
        self.running_total = previous_running + self.weighted_total()


    def scores(self):
        return [day.score if day else None for day in self.habit_days]


    def score_total(self):
        return sum([s for s in self.scores() if s is not None])


    def weighted_total(self):
        return self.score_total() / len([d for d in self.habit_days if d is not None])
