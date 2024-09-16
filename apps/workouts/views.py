from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import Workout
from .serializers import WorkoutSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from datetime import datetime, timedelta, date
import requests


def get_temperature(city_name, uf, date):
    KEY = 'b4a3ccab'
    response = requests.get(f"https://api.hgbrasil.com/weather?key={KEY}&city_name={city_name},{uf}&date={date}&mode=all&fields=only_results,time,temp,forecast,max,min,date")
    if response.status_code == 200:
        return response.json()
    return response.json(), response.status_code


def is_time_within_range(time):
    now = datetime.now().time()
    one_hour_back = (
        datetime.combine(datetime.today(), now) - timedelta(hours=1)
    ).time()
    one_hour_forward = (
        datetime.combine(datetime.today(), now) + timedelta(hours=1)
    ).time()
    return one_hour_back <= time <= one_hour_forward


@extend_schema(
    tags=["Workouts"],
    summary="Get instances of workouts.",
    description=\
        """This endpoint return each instance.""",
)
@api_view(['GET'])
def get(request):
    if request.method == 'GET':
        instances = Workout.objects.all()
        serializer = WorkoutSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        {"error": f"Invalid method."},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@extend_schema(
    tags=["Workouts"],
    summary="Post instance(s) of workouts.",
    description=\
        """This endpoint post a new instance.""",
    request=WorkoutSerializer,
    examples=[
        OpenApiExample(
            name='Minimum required',
            description='Only required fields.',
            value={
                "date": f"{date.today()}", 
                "kilometers": "10.00", 
                "duration": "00:60:00"
            }
        ),
        OpenApiExample(
            name='All fields except temperature',
            description='The system can only retrieve the temperature within a one-hour time window.',
            value={
                "date": f"{date.today()}", 
                "time_of_the_day": f"{datetime.now().strftime("%H:%M:%S")}",
                "city": "Rio de Janeiro",
                "state": "RJ",
                "kilometers": "10.00", 
                "duration": "00:60:00", 
                "frequency": 150,
                "kcal": 600,
            }
        ),
        OpenApiExample(
            name='All fields',
            description='When the temperature is provided, the system does not fetch it externally.',
            value={
                "date": f"{date.today()}", 
                "time_of_the_day": f"{datetime.now().strftime("%H:%M:%S")}",
                "city": "Rio de Janeiro",
                "state": "RJ",
                "kilometers": "10.00", 
                "duration": "00:60:00", 
                "frequency": 150,
                "kcal": 600,
                "temperature": "54"
            }
        ),
    ],
)
@api_view(['POST'])
def post(request):
    if request.method == 'POST':
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            time = serializer.validated_data.get('time_of_the_day', None)
            day = serializer.validated_data.get('date', None)
            city = serializer.validated_data.get('city', None)
            state = serializer.validated_data.get('state', None)
            temp = serializer.validated_data.get('temperature', None)
            if all([time, day, city, state]) and not temp:
                if day == date.today():
                    if is_time_within_range(time):
                        t = get_temperature(
                            city_name=city, 
                            uf=state, 
                            date=f"{date.today()}"
                        )
                        if 'temp' in t:
                            temp = t['temp']
            instance = serializer.save()
            if temp:
                instance.temperature = temp
                instance.save()
                return Response(
                    {"message": f"Saved."},
                    status=status.HTTP_200_OK
                )
            return Response(
                    {"message": f"Temperature not found. Saved without it."},
                    status=status.HTTP_200_OK
                )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"error": f"Invalid method."},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@extend_schema(
    tags=["Workouts"],
    summary="Update a instance of workouts.",
    description=\
        """This endpoint update a instance.""",
    request=WorkoutSerializer,
    examples=[
        OpenApiExample(
            name='Update location, date, and time to the current moment',
            description='Update location, date, and time to the current moment. The system can only retrieve the temperature within a one-hour time window.',
            value={
                "date": f"{date.today()}", 
                "time_of_the_day": f"{datetime.now().strftime("%H:%M:%S")}",
                "city": "Rio de Janeiro",
                "state": "RJ"
            }
        ),
        OpenApiExample(
            name='Update location, date, time, and also the temperature to the current moment.',
            description='Update location, date, and time to the current moment. The system saves the provided temperature.',
            value={
                "date": f"{date.today()}", 
                "time_of_the_day": f"{datetime.now().strftime("%H:%M:%S")}",
                "city": "Rio de Janeiro",
                "state": "RJ",
                "temperature": "100"
            }
        ),
        OpenApiExample(
            name='Update kilometers.',
            description='Update kilometers. The system will recalculate the speed.',
            value={
                "kilometers": "10.00"
            }
        ),
        OpenApiExample(
            name='Update duration.',
            description='Update duration. The system will recalculate the speed.',
            value={
                "duration": "02:00:00"
            }
        ),
    ],
)
@api_view(['PATCH'])
def update(request, pk):
    try:
        instance = Workout.objects.get(pk=pk)
    except Workout.DoesNotExist:
        return Response(
            {"error": f"Not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'PATCH':
        serializer = WorkoutSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            obj = serializer.save()
            data_day = serializer.validated_data.get('date', None)
            data_city = serializer.validated_data.get('city', None)
            data_state = serializer.validated_data.get('state', None)
            temp = serializer.validated_data.get('temperature', None)
            data_time = serializer.validated_data.get(
                'time_of_the_day', None
            )
            if (data_time or data_day or data_city or data_state) \
                and not temp:
                obj.temperature = None
                obj.save()
            if all([data_time, data_day, data_city, data_state]) \
                and not temp:
                if obj.date == date.today():
                    if is_time_within_range(obj.time_of_the_day):
                        t = get_temperature(
                            city_name=obj.city, 
                            uf=obj.state, 
                            date=f"{date.today()}"
                        )
                        if 'temp' in t:
                            obj.temperature = t['temp']
                            obj.save()
            return Response(
                {"message": f"Successfully."},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"error": f"Invalid method."},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
    

@extend_schema(
    tags=["Workouts"],
    summary="Delete a instance of workouts.",
    description="This endpoint delete a instance by pk."
)
@api_view(['DELETE'])
def delete(request, pk):
    try:
        instance = Workout.objects.get(pk=pk)
    except Workout.DoesNotExist:
        return Response(
            {"error": f"Not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'DELETE':
        instance.delete()
        return Response(
            {"message": f"Successfully."},
            status=status.HTTP_200_OK
        )
    return Response(
        {"error": f"Invalid method."},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
