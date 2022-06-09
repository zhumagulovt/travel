from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'password_confirm'
        ]
    
    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )
        user.create_activation_code()
        code = user.activation_code
        message = f'Активация почты: {user.email}\nКод: {code}'
        send_mail(
            'Активация почты',
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError("Неверный код")

        return data

    def activate_user(self):
        email = self.validated_data.get('email')

        user = User.objects.get(email=email)
        user.activation_code = ""
        user.is_active = True
        user.save()
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        request = self.context.get('request')
        
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь не существует")

        if not User.objects.get(email=email).is_active:
            raise serializers.ValidationError("Пользователь не активирован")

        user = authenticate(email=email, password=password, request=request)

        if user is None:
            raise serializers.ValidationError("Пароль неверный")

        data['user'] = user
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError("Старый пароль введен неверно")

        if old_password == new_password:
            raise serializers.ValidationError("Новый пароль похож на старый")
        
        return data

        