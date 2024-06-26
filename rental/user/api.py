from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rental.user.permissions import IsSelf
from rental.user.features import update_user, get_user
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rental.user.serializer import UpdateUserSerializer, UserDataSerializer
from rental.user.exceptions import validate_user_and_handle_errors
from settings.utils.exceptions import BadRequest400APIException
from rental.shared_serializers.serializers import UserProfileSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refreshToken"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=200)
        except Exception as e:
            raise BadRequest400APIException(str(e))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    user = request.user
    user = get_user(user.id)

    serialized_user = UserDataSerializer(user)

    return Response(serialized_user.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsSelf])
def update_profile(request):

    user = request.user
    serializer = UpdateUserSerializer(
        data={
            "id": user.id,
            "name": request.data.get("name"),
            "email": request.data.get("email"),
            "password": request.data.get("password"),
            "image": request.FILES.get("image"),
        }
    )
    validate_user_and_handle_errors(serializer)

    updated_user = update_user(
        user_id=user.id,
        name=serializer.validated_data.get("name"),
        email=serializer.validated_data.get("email"),
        password=serializer.validated_data.get("password"),
        image=serializer.validated_data.get("image"),
    )

    serialized_user = UserProfileSerializer(updated_user)

    return Response(serialized_user.data, status=status.HTTP_200_OK)
