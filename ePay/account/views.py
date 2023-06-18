from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer,UserRegisterSerializer,UserLoginSerializer,UserSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions,status
#from .validations import custom_validation
from rest_framework.views import APIView
from rest_framework import generics

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'message': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

@api_view(['POST'])
def user_register(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return JsonResponse({'message': 'Registration successful'})
    else:
        return Response(serializer.errors, status=400)

class UserRegister(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class =UserRegisterSerializer
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Do something with validated_data

        user = serializer.create(validated_data)
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(generics.GenericAPIView):
    
    serializer_class =UserLoginSerializer
    permission_classes=(permissions.AllowAny,)
    def get_queryset(self):
        pass
    def post(self,request):
        data=request.data
        print(data)
        test = {}
        test['email'] = data['email']
        test['password'] = data['password'] 
        print(test)
        #  assert UserRegisterSerializer.validate(data)
        serializer=UserLoginSerializer(data=test)
        if serializer.is_valid(raise_exception=True):
                user=serializer.check_user(request)
                login(request,user)
                return Response(data,status=status.HTTP_200_OK)
      

class UserLogout(APIView):
    def post(self,request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
class UserView(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(SessionAuthentication,)
    def get(self,request):
        serializer=UserSerializer(request.user)
        return Response({'user':serializer.data},status=status.HTTP_200_OK)


