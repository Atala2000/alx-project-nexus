from rest_framework import serializers
from .models import Job, Location, Application, JobPosting
from django.contrib.auth.models import User

class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.ReadOnlyField(source='posted_by.username')
    class Meta:
        model = Job
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    applied_by = serializers.ReadOnlyField(source='applied_by.username')
    class Meta:
        model = Application
        fields = '__all__'

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff']
        read_only_fields = ['is_staff'] 


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = False
        user.save()
        return user
