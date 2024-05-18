"""
Views for the course APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Course
from course import serializers


class CourseViewSet(viewsets.ModelViewSet):
    """View for manage course APIs."""
    serializer_class = serializers.CourseDetailSerializer
    queryset = Course.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve courses for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return serializer class for request."""
        if self.action == 'list':
            return serializers.CourseSerializer

        return self.serializer_class
