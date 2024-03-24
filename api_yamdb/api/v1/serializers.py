from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254
User = get_user_model()
username_validator = UnicodeUsernameValidator()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=(username_validator,)
    )

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        user.email_user(subject='Confirmation code', message=confirmation_code)
        return user

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user_by_username = User.objects.filter(username=username)
        user_by_email = User.objects.filter(email=email)
        if set(user_by_username) == set(user_by_email):
            return data
        if user_by_email:
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует!'
            )
        if user_by_username:
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует!'
            )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать me в качестве username запрещено!'
            )
        return value


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
