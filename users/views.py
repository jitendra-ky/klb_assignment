"""Views for the users app."""

from typing import ClassVar

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from .tasks import send_welcome_email


# Create your views here.
def index(request: Request) -> HttpResponse:
    """Index view for the users app.

    API Endpoints:
    1. GET    /                   - Index view (this page)
    2. POST   /api/register/      - Register a new user (public)
    3. GET    /api/profile/       - Get authenticated user's profile (protected)
    4. POST   /api/token/         - Obtain JWT token (public)
    5. POST   /api/token/refresh/ - Refresh JWT token (public)
    """
    return HttpResponse(
        f"""{request.method} {request.path} - Users API Index View
        <h2>Users API Endpoints</h2>
        <ul>
            <li><b>GET</b> <a href="/">/</a> - Index view (this page)</li>
            <li><b>POST</b> <a href="/api/register/">/api/register/</a> - Register a new user (public)</li>
            <li><b>GET</b> <a href="/api/profile/">/api/profile/</a> - Get authenticated user's profile (protected)</li>
            <li><b>POST</b> <a href="/api/token/">/api/token/</a> - Obtain JWT token (public)</li>
            <li><b>POST</b> <a href="/api/token/refresh/">/api/token/refresh/</a> - Refresh JWT token (public)</li>
        </ul>
        """,
    )


class RegisterView(APIView):
    """View to handle user registration."""

    def post(self, request: Request) -> Response:
        """Register a new user."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Send welcome email asynchronously
            send_welcome_email.delay(user.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    """View to retrieve the profile of the authenticated user."""

    permission_classes: ClassVar = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Get the profile of the authenticated user."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
