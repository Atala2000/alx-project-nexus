from django.contrib.auth.models import User
from rest_framework import viewsets, filters, generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    JobSerializer, LocationSerializer, ApplicationSerializer,
    JobPostingSerializer, UserSerializer
)
from .models import Job, Location, Application, JobPosting
from jobs.permissions import IsAdminOrReadOnly


# Simple admin check permission helper (we'll use is_staff)
class IsStaffUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'locations__city', 'company']
    ordering_fields = ['created_at', 'title']
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(posted_by=user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None):
        job = self.get_object()
        if request.user.is_staff:
            return Response(
                {"error": "Admins cannot apply for jobs."},
                status=status.HTTP_403_FORBIDDEN
            )
        application_data = {
            "job": job.id,
            "applicant_name": request.user.username,
            "applicant_email": request.user.email
        }
        serializer = ApplicationSerializer(data=application_data)
        if serializer.is_valid():
            serializer.save(applied_by=request.user)
            return Response({"message": "Application submitted successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['city', 'country']
    ordering_fields = ['city']

    def get_permissions(self):
        # Only admins can create/update/delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffUser()]
        return [AllowAny()]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['job__title', 'applicant_name', 'applicant_email']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(user=user)

    def get_permissions(self):
        # Only admins can list, retrieve, or delete applications
        if self.action in ['list', 'retrieve', 'destroy']:
            return [IsStaffUser()]
        # Any authenticated user can create an application
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(applied_by=self.request.user)


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['job__title', 'posted_date']
    ordering_fields = ['posted_date']

    def get_permissions(self):
        # Only admins can modify job postings
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffUser()]
        return [AllowAny()]


# Admin-only user management
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffUser]  # admin-only management


# Registration endpoint — currently public
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
