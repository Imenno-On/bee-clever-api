"""
Tests for course APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Course

from course.serializers import (
    CourseSerializer,
    CourseDetailSerializer,
)


COURSES_URL = reverse('course:course-list')


def detail_url(course_id):
    """Create and return a course detail URL."""
    return reverse('course:course-detail', args=[course_id])


def create_course(user, **params):
    """create and return a sample course."""
    defaults = {
        'title': 'Sample Course title',
        'duration_hours': 20,
        'price': Decimal('22.80'),
        'description': 'Sample Course description.',
        'link': 'http://example.com/',
    }
    defaults.update(params)

    course = Course.objects.create(user=user, **defaults)
    return course


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicCourseAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(COURSES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCourseAPITest(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_courses(self):
        """Test retrieving all courses."""
        create_course(user=self.user)
        create_course(user=self.user)

        res = self.client.get(COURSES_URL)

        courses = Course.objects.all().order_by('-id')
        serializer = CourseSerializer(courses, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_course_list_limited_to_user(self):
        """Test list of courses is limited to authenticated user."""
        other_user = create_user(
            email='other@example.com',
            password='password123'
        )
        create_course(user=other_user)
        create_course(user=self.user)

        res = self.client.get(COURSES_URL)

        courses = Course.objects.filter(user=self.user)
        serializer = CourseSerializer(courses, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_course_detail(self):
        """Test get course details."""
        course = create_course(user=self.user)

        url = detail_url(course.id)
        res = self.client.get(url)

        serializer = CourseDetailSerializer(course)
        self.assertEqual(res.data, serializer.data)

    def test_create_course(self):
        """Test creating a course."""
        payload = {
            'title': 'Sample Course',
            'duration_hours': 20,
            'price': Decimal('10.00')
        }
        res = self.client.post(COURSES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        course = Course.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(course, k), v)
        self.assertEqual(course.user, self.user)

    def test_partial_update(self):
        """Test partial update course."""
        original_link = 'https://example.com/course'
        course = create_course(
            user=self.user,
            title='Sample Course',
            link=original_link,
        )

        payload = {'title': 'New Course Title'}
        url = detail_url(course.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.title, payload['title'])
        self.assertEqual(course.link, original_link)
        self.assertEqual(course.user, self.user)

    def test_full_update(self):
        """Test full update course."""
        course = create_course(
            user=self.user,
            title='Sample course title',
            link='https://example.com/course',
            description='Sample course description.',
        )

        payload = {
            'title': 'New Course Title',
            'link': 'https://example.com/new-course',
            'description': 'New course description.',
            'duration_hours': 1000,
            'price': Decimal('12.34'),
        }
        url = detail_url(course.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(course, k), v)
        self.assertEqual(course.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the recipe user returns error."""
        new_user = create_user(email='user2@example.com', password='test12345')
        course = create_course(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(course.id)
        self.client.patch(url, payload)

        course.refresh_from_db()
        self.assertEqual(course.user, self.user)

    def test_delete_course(self):
        """Test deleting a course successful."""
        course = create_course(user=self.user)

        url = detail_url(course.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=course.id).exists())

    def test_delete_other_users_course_error(self):
        """Test trying to delete other users course returns error."""
        new_user = create_user(email='user2@example', password='pass12345')
        course = create_course(user=new_user)

        url = detail_url(course.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Course.objects.filter(id=course.id).exists())
