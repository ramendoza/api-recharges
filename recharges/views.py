from requests import RequestException
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api_client import fetch_recharge_prices, fetch_send_recharges, send_recharge
from .serializers import RechargeSerializer, SendRechargeSerializer, UserDataSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]


class SendRechargesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = fetch_send_recharges()
        except RequestException as exc:
            return Response(
                {"detail": "Failed to fetch send recharges", "error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response(data)


class RechargePricesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = fetch_recharge_prices(request.user)
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except RequestException as exc:
            return Response(
                {"detail": "Failed to fetch recharge prices", "error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        serializer = RechargeSerializer(data, many=True)
        return Response(serializer.data)


class SendRechargeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendRechargeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            data = send_recharge(
                {
                    "recharge": serializer.validated_data.get("product"),
                    "sendTo": [f"53{serializer.validated_data.get('send_to')}"],
                },
                request.user,
            )
        except RequestException as exc:
            print(exc)
            return Response(
                {"detail": "Failed to send recharge", "error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response(data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDataSerializer(user)
        return Response(serializer.data)
