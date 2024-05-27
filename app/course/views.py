"""
Views for the course APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Course,
    Tag,
)
from course import serializers


class CourseViewSet(viewsets.ModelViewSet):
    """View for manage course APIs."""
    serializer_class = serializers.CourseDetailSerializer
    queryset = Course.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_inits(self, qs):
        """Convert a list of string to integers"""
        return [int(str_id) for str_id in qs.split(',')]


    def get_queryset(self):
        """Retrieve courses for authenticated user."""
        tags = self.request.query_params.get('tags')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_inits(tags)
            queryset = queryset.filter(tags__id__in=tags_ids)
        return self.queryset.filter(user=self.request.user).order_by('id').distinct()

    def get_serializer_class(self):
        """Return serializer class for request."""
        if self.action == 'list':
            return serializers.CourseSerializer
        elif self.action == 'upload_image':
            return serializers.CourseImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new course."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to course."""
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
