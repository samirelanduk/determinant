from datetime import datetime, time, date
from mixer.backend.django import mixer
from testarsenal import DjangoTest
from determinant.models import *


class HabitTests(DjangoTest):

    def test_can_create_habit(self):
        habit = Habit(
         name="habit", description="DDD", start_date=date(1990, 9, 30),
         reward="1", penalty="2", cheat="4"
        )
        habit.full_clean()


    def test_can_get_cheats(self):
        habit = Habit(
         name="habit", description="DDD", start_date=date(1990, 9, 30),
         reward="1", penalty="2", cheat="4"
        )
        self.assertEqual(habit.cheats(), [4])
        habit.cheat = "4,7"
        self.assertEqual(habit.cheats(), [4, 5, 6, 7])
        habit.cheat = "4,7,2"
        self.assertEqual(habit.cheats(), [4, 5, 6, 7, 6, 5, 4, 3, 2])
