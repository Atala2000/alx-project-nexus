from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    JobViewSet, LocationViewSet, ApplicationViewSet, JobPostingViewSet,
    UserViewSet, RegisterView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='job')
router.register('locations', LocationViewSet, basename='location')
router.register('applications', ApplicationViewSet, basename='application')
router.register('job-postings', JobPostingViewSet, basename='jobposting')
router.register('users', UserViewSet, basename='user')  

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
