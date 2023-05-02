from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from flights_app.serializers import SignupSerializer, UserSerializer


# Create your views here.


@api_view(['POST'])
def signup(request):
    signup_serializer = SignupSerializer(data=request.data, many=False)
    if signup_serializer.is_valid(raise_exception=True):

        # only staff can create staff
        if signup_serializer.validated_data['is_staff']:
            if not (request.user.is_authenticated and request.user.is_staff):
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={'is_staff': ['Only staff member can create staff user']})

        new_user = signup_serializer.create(signup_serializer.validated_data)
        user_serializer = UserSerializer(instance=new_user, many=False)
        return Response(data=user_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user_serializer = UserSerializer(instance=request.user, many=False)
    return Response(data=user_serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user(request):
    all_user = User.objects.all()
    serializer = UserSerializer(instance=all_user, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_users_by_name(request):
    users = request.GET.get('q')
    if users:
        users = User.objects.filter(Q(username__icontains=users) | Q(first_name__icontains=users) | Q(last_name__icontains=users))
    else:
        users = User.objects.all()

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)



