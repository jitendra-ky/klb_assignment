"""Views for the users app."""

from typing import ClassVar
from urllib.request import Request

from django.shortcuts import HttpResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


# Create your views here.
def index(request: Request) -> HttpResponse:
    """Index view for the users app."""
    return HttpResponse(f"Hello, world. You're at the users index. {request}")


class RegisterView(APIView):
    """View to handle user registration."""

    def post(self, request: Request) -> Response:
        """Register a new user."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    """View to retrieve the profile of the authenticated user."""

    permission_classes: ClassVar = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Get the profile of the authenticated user."""
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
        })
