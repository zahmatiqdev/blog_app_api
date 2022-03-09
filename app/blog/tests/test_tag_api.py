from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from blog.serializers import TagSerializer


TAG_URL = reverse('blog:tag-list')


def sample_tag(user, name='news'):
    """Create and return sample tag"""
    return Tag.objects.create(user=user, name=name)


def detail_url_tag(tag_id):
    """return tag detail url"""
    return reverse('blog:tag-detail', args=[tag_id])


class PublicTagApiTest(TestCase):
    """Test Tag object in Public mode"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    """Test the authorized user tags api"""

    def setUp(self):
        self.user = get_user_model().objects.create_staffuser(
            email='test@gmail.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='feedback')
        Tag.objects.create(user=self.user, name='community')

        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'user': self.user, 'name': 'laptop'}
        res = self.client.post(TAG_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_update_tag_successful(self):
        """Test updating one row data"""
        tag = sample_tag(self.user, name='laptop')

        payload = {'user': self.user, 'name': 'tech'}
        res = self.client.put(detail_url_tag(tag.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        exists = Tag.objects.filter(name='tech').exists()
        self.assertTrue(exists)

    def test_delete_tag_successful(self):
        """Test deleting one row data"""
        tag = sample_tag(self.user, name='laptop')
        res = self.client.delete(detail_url_tag(tag.id))
        exists = Tag.objects.filter(name='laptop').exists()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)

    def test_duplicate_tag_fail(self):
        """Fail to creating duplicate tag"""
        name = 'laptop'
        sample_tag(self.user, name=name)

        res = self.client.post(TAG_URL, {'user': self.user, 'name': 'Laptop'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
