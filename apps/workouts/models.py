from django.db import models


class State(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]


class Workout(models.Model):

    date = models.DateField(auto_now=False, auto_now_add=False)
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True)
    kilometers = models.DecimalField(max_digits=7, decimal_places=2)
    duration = models.DurationField()
    bpm = models.IntegerField()
    kcal = models.IntegerField()
    # bpm = models.CharField(max_length=16)
    # kcal = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.date} - {self.kilometers} ({self.state})'

    class Meta:
        ordering = ["date"]
