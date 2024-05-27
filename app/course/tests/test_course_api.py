"""
Tests for course APIs.
"""
from decimal import Decimal
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Course,
    Tag,
)

from course.serializers import (
    CourseSerializer,
    CourseDetailSerializer,
)


COURSES_URL = reverse('course:course-list')


def detail_url(course_id):
    """Create and return a course detail URL."""
    return reverse('course:course-detail', args=[course_id])


def image_upload_url(course_id):
    """Create and return a course detail URL."""
    return reverse('course:course-upload-image', args=[course_id])


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
        """Test changing the course user returns error."""
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

    def test_create_course_with_new_tags(self):
        """Test creating a course with new tags."""
        payload = {
            'title': 'Harvard CS109',
            'duration_hours': 35,
            'price': Decimal('99.99'),
            'tags': [{'name': 'Computer Science'}, {'name': 'Harvard'}],
        }
        res = self.client.post(COURSES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        courses = Course.objects.filter(user=self.user)
        self.assertEqual(courses.count(), 1)
        course = courses[0]
        self.assertEqual(course.tags.count(), 2)
        for tag in payload['tags']:
            exists = course.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_course_with_existing_tags(self):
        """Test creating a course with existing tag."""
        tag_python = Tag.objects.create(user=self.user, name='Python')
        payload = {
            'title': 'Python Generation',
            'duration_hours': 15,
            'price': Decimal('0'),
            'tags': [{'name': 'Python'}, {'name': 'Free'}],
        }
        res = self.client.post(COURSES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        courses = Course.objects.filter(user=self.user)
        self.assertEqual(courses.count(), 1)
        course = courses[0]
        self.assertEqual(course.tags.count(), 2)
        self.assertIn(tag_python, course.tags.all())
        for tag in payload['tags']:
            exists = course.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        """Test creating a tag on update of a course."""
        course = create_course(user=self.user)

        payload = {'tags': [{'name': 'Python'}]}
        url = detail_url(course.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='Python')
        self.assertIn(new_tag, course.tags.all())

    def test_update_course_assign_tag(self) -> object:
        """Test assigning an existing tag when updating a course."""
        tag_html = Tag.objects.create(user=self.user, name='HTML')
        course = create_course(user=self.user)
        course.tags.add(tag_html)

        tag_css = Tag.objects.create(user=self.user, name='CSS')
        payload = {'tags': [{'name': 'CSS'}]}
        url = detail_url(course.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_css, course.tags.all())
        self.assertNotIn(tag_html, course.tags.all())

    def test_clear_course_tags(self):
        """Test clearing a course tags."""
        tag = Tag.objects.create(user=self.user, name='HTML')
        course = create_course(user=self.user)
        course.tags.add(tag)

        payload = {'tags': []}
        url = detail_url(course.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(course.tags.count(), 0)


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123'
        )
        self.client.force_authenticate(self.user)
        self.course = create_course(user=self.user)

    def tearDown(self):
        self.course.image.delete()

    def test_upload_image(self):
        """Test uploading ann image to a course."""
        url = image_upload_url(self.course.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10,10))
            img.save(image_file, format = 'JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format = 'multipart')

        self.course.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.course.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url(self.course.id)
        payload = {'image':'notanimage'}
        res = self.client.post(url, payload, format = 'multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)