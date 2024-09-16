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
        data = {
            "date": TODAY, "kilometers": "10.00", "duration": "00:60:00", 
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
        data = {
            "date": TODAY, 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
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
        With correctly date, time, city and state fields
        """
        instant = datetime.now()
        data = {
            "date": TODAY, 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "city": "Rio de Janeiro", 
            "state": "RJ", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
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


    def test_post_005(self):
        """
        Date is not today, date in the past
        """
        instant = datetime.now()
        data = {
            "date": "1990-05-29", 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "city": "Rio de Janeiro", 
            "state": "RJ", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
        }
        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(MODEL.objects.all().count(), 1)
        obj = MODEL.objects.all().first()
        self.assertEqual(obj.date, date(1990, 5, 29))
        self.assertEqual(obj.time.replace(microsecond=0), instant.time().replace(microsecond=0))
        self.assertEqual(obj.city, "Rio de Janeiro")
        self.assertEqual(obj.state, "RJ")
        self.assertEqual(obj.kilometers, Decimal('10.00'))
        self.assertEqual(obj.duration, timedelta(seconds=3600))
        self.assertEqual(obj.frequency, None)
        self.assertEqual(obj.kcal, None)
        self.assertIsNone(obj.temperature)
        self.assertEqual(obj.speed, Decimal('10.00'))
        obj = MODEL.objects.all().delete()

    
    def test_post_006(self):
        """
        Date is not today, date in the future
        """
        instant = datetime.now()
        data = {
            "date": "2170-05-29", 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "city": "Rio de Janeiro", 
            "state": "RJ", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
        }
        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)


    def test_post_007(self):
        """
        Time is not now, time with more one hour
        """
        instant = datetime.now() + timedelta(hours=1, minutes=1)
        data = {
            "date": TODAY, 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "city": "Rio de Janeiro", 
            "state": "RJ", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
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
        self.assertIsNone(obj.temperature)
        self.assertEqual(obj.speed, Decimal('10.00'))
        obj = MODEL.objects.all().delete()
    

    def test_post_008(self):
        """
        Tiume is not now, time with less one hour
        """
        instant = datetime.now() - timedelta(hours=1, minutes=1)
        data = {
            "date": TODAY, 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "city": "Rio de Janeiro", 
            "state": "RJ", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
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
        self.assertIsNone(obj.temperature)
        self.assertEqual(obj.speed, Decimal('10.00'))
        obj = MODEL.objects.all().delete()


    def test_post_009(self):
        """
        With incorrectly or city or state fields
        """
        instant = datetime.now()
        data = {
            "date": TODAY, 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "city": "Incorrectly", 
            "state": "MG", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
        }
        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(MODEL.objects.all().count(), 1)
        obj = MODEL.objects.all().first()
        self.assertEqual(obj.date, date.today())
        self.assertEqual(obj.time.replace(microsecond=0), instant.time().replace(microsecond=0))
        self.assertEqual(obj.city, "Incorrectly")
        self.assertEqual(obj.state, "MG")
        self.assertEqual(obj.kilometers, Decimal('10.00'))
        self.assertEqual(obj.duration, timedelta(seconds=3600))
        self.assertEqual(obj.frequency, None)
        self.assertEqual(obj.kcal, None)
        self.assertIsNotNone(obj.temperature)
        self.assertEqual(obj.speed, Decimal('10.00'))
        obj = MODEL.objects.all().delete()
    

    def test_post_010(self):
        """
        With incorrectly or city or state fields
        """
        instant = datetime.now()
        data = {
            "date": TODAY, 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "city": "Rio de Janeiro", 
            "state": "SP", 
            "kilometers": "10.00", 
            "duration": "00:60:00", 
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
        self.assertEqual(obj.state, "SP")
        self.assertEqual(obj.kilometers, Decimal('10.00'))
        self.assertEqual(obj.duration, timedelta(seconds=3600))
        self.assertEqual(obj.frequency, None)
        self.assertEqual(obj.kcal, None)
        self.assertIsNotNone(obj.temperature)
        self.assertEqual(obj.speed, Decimal('10.00'))
        obj = MODEL.objects.all().delete()

    
    def test_post_011(self):
        """
        Incorrectly format of the date
        """
        instant = datetime.now()
        data = {
            "date": "24-09-01", 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "kilometers": "10.00", 
            "duration": "00:60:00", 
        }
        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)

    
    def test_post_012(self):
        """
        Incorrectly format of the time
        """
        data = {
            "date": TODAY, 
            "time": "00h01",
            "kilometers": "10.00", 
            "duration": "00:60:00", 
        }
        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)
    

    def test_post_013(self):
        """
        Incorrectly format of the kilometer
        """
        instant = datetime.now()
        data = {
            "date": TODAY, 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "kilometers": "10,00", 
            "duration": "00:60:00", 
        }
        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)


    def test_post_014(self):
        """
        Incorrectly format of the duration
        """
        instant = datetime.now()
        data = {
            "date": TODAY, 
            "time": f"{instant.strftime("%H:%M:%S")}",
            "kilometers": "10.00", 
            "duration": "00:60", 
        }
        request = self.client.post(
            reverse(URL_POST), data, content_type='application/json'
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(MODEL.objects.all().count(), 0)
