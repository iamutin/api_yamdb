from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

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
        if value.lower() == 'me':
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

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать me в качестве username запрещено!'
            )
        return value


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_null=False,
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def to_representation(self, title):
        serializer = TitleSerializer(title)
        return serializer.data

    def validate_year(self, year):
        current_year = timezone.now().year
        if year > current_year:
            raise serializers.ValidationError(
                f'Год выпуска не может быть больше {current_year}.'
            )
        return year


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            author = request.user
            title = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв к этому произведению'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
