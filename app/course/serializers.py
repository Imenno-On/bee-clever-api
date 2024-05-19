"""
Serializers for course APIs
"""
from rest_framework import serializers

from core.models import (
    Course,
    Tag,
)


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for courses."""

    class Meta:
        model = Course
        fields = ['id', 'title', 'duration_hours', 'price', 'link']
        read_only_fields = ['id']


class CourseDetailSerializer(CourseSerializer):
    """Serializer for course detail view."""

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['description']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
