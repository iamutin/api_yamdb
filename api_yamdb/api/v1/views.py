from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (TokenObtainSerializer,
                          UserCreateSerializer,
                          UserSerializer)

User = get_user_model()


class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            message = {'token': str(AccessToken.for_user(user))}
            return Response(message, status=status.HTTP_200_OK)
        message = {'confirmation_code': 'Неверный код подтверждения'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = UserSerializer
    lookup_field = 'username'
