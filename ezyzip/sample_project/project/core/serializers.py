from unicodedata import name
from . models import Client
from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"error": "Password is not matching"})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'created_by', 'created_on']
        read_only_fields = ['id', 'created_by',
                            'created_on', 'modified_by', 'modified_on']

    def create(self, validated_data):
        print("sace")
        client = Client.objects.create(
            name=validated_data["name"],
            created_by=self.context['request'].user.username
        )
        client.save()
        return client

class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'project', 'created_by',
                  'created_on', 'modified_by', 'modified_on']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'project', 'users', 'created_by',
                  'created_on']
