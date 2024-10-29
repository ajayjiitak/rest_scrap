from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer

# Create your views here.
# class RegisterView(generics.CreateAPIView):
#     queryset= User.objects.all()
#     permission_classes=(AllowAny,)
#     serializer_class=RegisterSerializer

# class LoginView(generics.GenericAPIView):
#     serializer_class=LoginSerializer

#     def post(self,request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             user_serializer=UserSerializer(user)
#             return Response({
#                 'refresh':str(refresh),
#                 'access':str(refresh.access_token),
#                 'user':user_serializer.data
#             })
#         else:
#             return Response({'detail':'ivalid credentails'},status=401)
        
# class DashboardView(APIView):
#     permission_classes=(IsAuthenticated,)
#     def get(self,request):
#         user=request.user
#         user_serializer = UserSerializer(user)
#         return Response({
#             'message':'varanm varanm mr indrachoodan',
#             'user':user_serializer.data

#         },200)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .tasks import yahoo_auction_scrape_task, merukari_scrape_task

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# class LoginView(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)  # Validate incoming data

#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             user_serializer = UserSerializer(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': user_serializer.data
#             })
#         else:
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Deserialize and validate the incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class DashboardView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'Welcome to your dashboard!',
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)

class SimpleScrapeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        url = request.data.get("url")
        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Call the Celery task for Yahoo Auction scraping
        yahoo_auction_scrape_task.delay(url=url)
        return Response({"message": "Yahoo Auction scraping started."}, status=status.HTTP_202_ACCEPTED)

class DetailedScrapeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        platform = request.data.get("platform")
        url = request.data.get("url")
        product_id = request.data.get("product_id")

        if platform == "yahoo" and url:
            yahoo_auction_scrape_task.delay(url=url)
            return Response({"message": "Yahoo Auction scraping started."}, status=status.HTTP_202_ACCEPTED)

        elif platform == "merukari" and product_id:
            merukari_scrape_task.delay(product_id=product_id)
            return Response({"message": "MeruKari scraping started."}, status=status.HTTP_202_ACCEPTED)

        return Response({"error": "Invalid platform or parameters"}, status=status.HTTP_400_BAD_REQUEST)      