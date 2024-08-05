from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers,generics, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

    def validate(self, attrs):
        # The original validate method returns a dict with the token
        data = super().validate(attrs)

        # Add custom data to the response
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
            'user_id': self.user.id,
            # Add more fields as necessary
        }

        return data

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    user_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'user_id')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    def delete(self, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)