from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import Workout
from .serializers import WorkoutSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from datetime import datetime, timedelta, date
from .api_outside import get_temperature


# def time_on_time(time):
#     now = datetime.now().time()
#     one_hour_back = (
#         datetime.combine(datetime.today(), now) - timedelta(hours=1)
#     ).time()
#     one_hour_forward = (
#         datetime.combine(datetime.today(), now) + timedelta(hours=1)
#     ).time()
#     return one_hour_back <= time <= one_hour_forward


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
            name='New register of one instance',
            description='',
            value={
                "date": f"{date.today()}", 
                "time": f"{datetime.now().strftime("%H:%M:%S")}",
                "city": "Rio de Janeiro",
                "state": "RJ",
                "kilometers": "10.00", 
                "duration": "00:60:00", 
                "frequency": 150,
                "kcal": 600,
            }
        ),
    ],
)
@api_view(['POST'])
def post(request):
    if request.method == 'POST':
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            time = serializer.validated_data.get('time', None)
            day = serializer.validated_data.get('date', None)
            city = serializer.validated_data.get('city', None)
            state = serializer.validated_data.get('state', None)
            temperature = None
            if time and date and city and state:
                if day == date.today():
                    now = datetime.now().time()
                    one_hour_back = (
                        datetime.combine(
                            datetime.today(), now) - timedelta(hours=1)
                    ).time()
                    one_hour_forward = (
                        datetime.combine(
                            datetime.today(), now) + timedelta(hours=1)
                    ).time()
                    if one_hour_back <= time <= one_hour_forward:
                        t = get_temperature(
                            city_name=city, uf=state, date=date
                        )
                        if 'temp' in t:
                            temperature = t['temp']
            instance = serializer.save()
            if temperature:
                instance.temperature = temperature
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
            name='Update a instance by pk',
            description='An instance must be created previously.',
            value={
                '???': '???',
                '???': '???'
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
            serializer.save()
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
