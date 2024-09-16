from django.db import models
from decimal import Decimal


class Workout(models.Model):

    date = models.DateField(auto_now=False, auto_now_add=False)
    time_of_the_day = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    state = models.CharField(max_length=32, blank=True, null=True)
    kilometers = models.DecimalField(max_digits=7, decimal_places=2)
    duration = models.DurationField()
    frequency = models.IntegerField(blank=True, null=True)
    kcal = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    speed = models.DecimalField(
        max_digits=7, decimal_places=2, editable=False
    )

    def __str__(self):
        return f'{self.date} - {self.kilometers} ({self.city}, {self.state})'

    class Meta:
        ordering = ["date"]

    def speed_calc(self):
        if self.duration.total_seconds() > 0:
            duration_in_hours = Decimal(self.duration.total_seconds()) / Decimal(3600)
            self.speed = self.kilometers / duration_in_hours
        else:
            self.speed = Decimal(0)

    def save(self, *args, **kwargs):
        self.speed_calc()
        super().save(*args, **kwargs)
