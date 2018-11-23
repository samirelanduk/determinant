from django.db import models

class Habit(models.Model):

    name = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateField()
    reward = models.CharField(max_length=16)
    penalty = models.CharField(max_length=16)
    cheat = models.CharField(max_length=32)



class Record(models.Model):

     habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
     date = models.DateField()
     success = models.BooleanField()
