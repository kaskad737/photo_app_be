from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from authapp.models import User
from django.contrib.auth.password_validation import validate_password
from .utils import password_validation


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password1 = serializers.CharField(write_only=True, required=True,
                                      validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Password fields didn\'t match.'
            })

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password1'])
        user.save()

        return user


class InvitationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'pk', 'username'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PasswordCheckAndSetSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        min_length=8,
        max_length=64,
        write_only=True,
        required=True,
    )
    password2 = serializers.CharField(
        min_length=8,
        max_length=64,
        write_only=True,
        required=True,
    )
    invitation = serializers.CharField(required=True)

    class Meta:
        fields = ["password1", "password2"]

    def validate(self, attrs):
        """
        Validate the provided attributes.

        Checks if the provided passwords match and are valid.
        """
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise exceptions.AuthenticationFailed({"message": "The passwords don't match. Please try again."})

        password_validation(password=password1)

        return attrs


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
