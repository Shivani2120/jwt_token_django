from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer  # Corrected import
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
def user_register_view(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)  # Corrected serializer name

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'Account has been created'
            data['username'] = account.username
            data['email'] = account.email

            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors

        return Response(data)

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def logout_user(request):
    if request.method == "POST":
        # Check if the user has an associated auth_token
        if hasattr(request.user, 'auth_token') and request.user.auth_token:
            request.user.auth_token.delete()
            return Response({"message": "You are logged out"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User does not have an authentication token"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


