from rest_framework import serializers

from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'nick_name', 'date_of_birth', 'phone', 'gender', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = True
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Both email and password are required.')

        attrs['user'] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

    def send_reset_code(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)

        reset_code = random.randint(1000, 9999)
        user.reset_code = reset_code
        user.save()

        send_mail(
            'Password Reset Code',
            f'Your password reset code is: {reset_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        reset_code = data.get("reset_code")

        try:
            user = CustomUser.objects.get(email=email, reset_code=reset_code)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid reset code or email.")
        
        return data

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        user = CustomUser.objects.get(email=email)
        user.set_password(new_password)
        user.reset_code = None 
        user.save()
        return user
