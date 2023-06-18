from django.forms import ValidationError
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'para_birimi_secimi']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email', 'password', 'first_name', 'last_name', 'para_birimi_secimi']
    def create(self, validated_data):
        user_obj=CustomUser.objects.create_user(**validated_data)

        user_obj.save()
        return user_obj
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Email doğrulama
        if email:
            if CustomUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("Bu e-posta adresi zaten kullanılıyor.")

        # Şifre doğrulama
        if password:
            if len(password) < 8:
                raise serializers.ValidationError("Şifre en az 8 karakter uzunluğunda olmalıdır.")

        return data
from django.contrib.auth import authenticate

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        email = clean_data.data['email']
        password = clean_data.data['password']
        print(CustomUser.objects.filter(email = email))
        user = authenticate(request=clean_data,email=email,password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        return user

    def authenticate_user(self, email, password):
        UserModel = get_user_model()
        user = None
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
         model = CustomUser
         fields = ['email', 'first_name', 'last_name', 'para_birimi_secimi']