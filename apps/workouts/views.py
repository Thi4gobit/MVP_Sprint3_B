from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import Workout
from .serializers import WorkoutSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
import requests


def get_temperature(city_name, uf, date, time_hour):
    KEY = 'b4a3ccab'
    response = requests.get(f"https://api.hgbrasil.com/weather?key={KEY}&city_name={city_name},{uf}&date={date}&date=hourly")
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Erro: {response.status_code}")


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
                '???': '???',
                '???': '???'
            }
        ),
    ],
)
@api_view(['POST'])
def post(request):
    if request.method == 'POST':
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():

            serializer.validated_data.get('', None)

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
