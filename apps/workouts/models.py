from django.db import models


class Workout(models.Model):

    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
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
            duration_in_hours = self.duration.total_seconds() / 3600
            self.speed = self.kilometers / duration_in_hours
        else:
            self.speed = 0
        self.save()

    def save(self, *args, **kwargs):
        self.speed_calc()
        super().save(*args, **kwargs)
