#from crypt import methods
from http import client
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import login
from . import serializers
from core.models import Client
from rest_framework.decorators import action
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.shortcuts import get_object_or_404

# Create your views here.


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        return False


class LoginAPI(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = User.objects.all()
        serializer = serializers.UserSerializer(queryset, many=True)
        return Response(serializer.data,200)


    def create(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.username = request.data["username"]
        user.email = request.data["email"]
        user.save()
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=204)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ClientDetailSerializer

    @action(url_path="project", methods=["post"], detail=False)
    def project_post(self, request, *args, **kwargs):
        try:

            clinet = Client.objects.get(id=kwargs['id'])
            clinet.project = request.data["project"]
            clinet.user = request.data["users"]
            client.created_by= self.request.user
            clinet.save()
            return Response(request.data, 200)
        except Exception as e:
            print("error", e)
            return Response({"error": "Record Not Found"}, 404)


class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Client.objects.all()
        serializer = serializers.ProjectSerializer(queryset, many=True)
        return Response(serializer.data)
