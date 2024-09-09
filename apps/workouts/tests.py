from django.test import TestCase
from django.urls import reverse
from .models import Workout
from datetime import timedelta, datetime, date
from decimal import Decimal


MODEL = Workout
URL_POST = 'workout_post'
TODAY = f"{date.today()}"


class PostTestCase(TestCase):


    def test_post_001(self):
        """
        Only required fields
        """
        #{"date": "2024-09-01","kilometers": "10.01","duration": "50:05:00"}
        data = {
            "date": TODAY, 
            #"time": "10:00", 
            #"city": "Rio de Janeiro", 
            #"state": "RJ", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
            #"frequency": "150", 
            #"kcal": "600", 
            #"temperature": "", 
            #"speed": "30", 
        }
        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(MODEL.objects.all().count(), 1)
        obj = MODEL.objects.all().first()
        self.assertEqual(obj.date, date.today())
        self.assertEqual(obj.time, None)
        self.assertEqual(obj.city, None)
        self.assertEqual(obj.state, None)
        self.assertEqual(obj.kilometers, Decimal('10.00'))
        self.assertEqual(obj.duration, timedelta(seconds=3600))
        self.assertEqual(obj.frequency, None)
        self.assertEqual(obj.kcal, None)
        self.assertEqual(obj.temperature, None)
        self.assertEqual(obj.speed, Decimal('10.00'))
        obj = MODEL.objects.all().delete()

    
    def test_post_002(self):
        """
        Whitout the required fields (null or blank)
        """
        data1 = {
            "date": "", "kilometers": "10.00", "duration": "00:60:00", 
        }
        data2 = {
            "date": TODAY, "kilometers": "", "duration": "00:60:00", 
        }
        data3 = {
            "date": TODAY, "kilometers": "10.00", "duration": "", 
        }
        data4 = {
            "kilometers": "10.00", "duration": "00:60:00", 
        }
        data5 = {
            "date": TODAY, "duration": "00:60:00", 
        }
        data6 = {
            "date": TODAY, "kilometers": "10.00", 
        }
        request = self.client.post(
            reverse(URL_POST), data1, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)
        request = self.client.post(
            reverse(URL_POST), data2, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)
        request = self.client.post(
            reverse(URL_POST), data3, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)
        request = self.client.post(
            reverse(URL_POST), data4, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)
        request = self.client.post(
            reverse(URL_POST), data5, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)
        request = self.client.post(
            reverse(URL_POST), data6, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)


    def test_post_003(self):
        """
        Ignore speed field
        """
        #{"date": "2024-09-01","kilometers": "10.01","duration": "50:05:00"}
        data = {
            "date": TODAY, 
            #"time": "10:00", 
            #"city": "Rio de Janeiro", 
            #"state": "RJ", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
            #"frequency": "150", 
            #"kcal": "600", 
            #"temperature": "", 
            "speed": "30", 
        }
        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(MODEL.objects.all().count(), 1)
        obj = MODEL.objects.all().first()
        self.assertEqual(obj.date, date.today())
        self.assertEqual(obj.time, None)
        self.assertEqual(obj.city, None)
        self.assertEqual(obj.state, None)
        self.assertEqual(obj.kilometers, Decimal('10.00'))
        self.assertEqual(obj.duration, timedelta(seconds=3600))
        self.assertEqual(obj.frequency, None)
        self.assertEqual(obj.kcal, None)
        self.assertEqual(obj.temperature, None)
        self.assertEqual(obj.speed, Decimal('10.00'))
        obj = MODEL.objects.all().delete()

    
    def test_post_004(self):
        """
        With time, city and state fields
        """
        #{"date": "2024-09-01","kilometers": "10.01","duration": "50:05:00"}
        instant = datetime.now()
        data = {
            "date": TODAY, 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "city": "Rio de Janeiro", 
            "state": "RJ", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
            #"frequency": "150", 
            #"kcal": "600", 
            #"temperature": "", 
            "speed": "30", 
        }

        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 200)
        
        self.assertEqual(MODEL.objects.all().count(), 1)
        obj = MODEL.objects.all().first()
        self.assertEqual(obj.date, date.today())
        self.assertEqual(obj.time.replace(microsecond=0), instant.time().replace(microsecond=0))
        self.assertEqual(obj.city, "Rio de Janeiro")
        self.assertEqual(obj.state, "RJ")
        self.assertEqual(obj.kilometers, Decimal('10.00'))
        self.assertEqual(obj.duration, timedelta(seconds=3600))
        self.assertEqual(obj.frequency, None)
        self.assertEqual(obj.kcal, None)
        self.assertIsNotNone(obj.temperature)
        self.assertEqual(obj.speed, Decimal('10.00'))

        obj = MODEL.objects.all().delete()
