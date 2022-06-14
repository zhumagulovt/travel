from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView

from .serializers import RegistrationSerializer, ActivationSerializer,\
    LoginSerializer, PasswordChangeSerializer, SavedTourSerializer

from tours.models import Tour
from tours.serializers import TourSerializer


class RegistrationView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(
                "Новый пользователь создан", 
                status=status.HTTP_201_CREATED
            )
        

class ActivationView(APIView):

    def post(self, request):
        data = request.data
        serializer = ActivationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.activate_user()

        return Response(
            "Пользователь активирован",
            status=status.HTTP_200_OK
        )


class LoginView(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key},
            status=status.HTTP_200_OK
        )


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        serializer = PasswordChangeSerializer(data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()
        user.auth_token.delete()
        return Response(
            "Пароль изменен", 
            status=status.HTTP_200_OK
        )


class SavedView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TourSerializer

    def get_queryset(self):
        user = self.request.user
        saved = user.saved.values('tour_id')
        queryset = Tour.objects.filter(id__in=saved)
        return queryset


class ToursHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TourSerializer

    def get_queryset(self):
        user = self.request.user
        history_tours = user.tours_history.values('tour_id')
        queryset = Tour.objects.filter(id__in=history_tours)
        return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response(
        "Пользователь вышел из аккаунта", 
        status=status.HTTP_200_OK
    )
