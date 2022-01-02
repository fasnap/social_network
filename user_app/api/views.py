from rest_framework.response import Response
from user_app.api.serializers import UserRegistrationSerializer, UserSerializer
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class user_registration_view(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['fullname'] = self.user.fullname
        data['email'] = self.user.email
        data['phone'] = self.user.phone
        data['id']=self.user.id
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# class TokenObtainPairView(APIView):
#     def post(self, request, format=None):
#         token_user_email = request.user.email
#         token_user_username = request.user.username
#         pass
    

# class APILogoutView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         if self.request.data.get('all'):
#             token: OutstandingToken
#             for token in OutstandingToken.objects.filter(user=request.user):
#                 _, _ = BlacklistedToken.objects.get_or_create(token=token)
#             return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
#         refresh_token = self.request.data.get('refresh_token')
#         token = RefreshToken(token=refresh_token)
#         token.blacklist()
#         return Response({"status": "OK, goodbye"})
# from user_app.api.serializers import UserRegistrationSerializer
# from rest_framework.response import Response 
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.decorators import api_view

# @api_view(['POST',])
# def user_registration_view(request):

#     if request.method == 'POST':
#         serializer = UserRegistrationSerializer(data=request.data)

#         data = {}

#         if serializer.is_valid():
#             account = serializer.save()

#             data['response'] = 'Registration successful'
#             data['username'] = account.username
#             data['email'] = account.email
#             data['fullname'] = account.fullname
#             data['phone'] = account.phone
            
#             refresh = RefreshToken.for_user(account)
#             data['token'] = {
#                 'refresh': str(refresh),
#                 'access':str(refresh.access_token),
#             }

#         else:
#             data = serializer.errors
        
        
#         return Response(data)
