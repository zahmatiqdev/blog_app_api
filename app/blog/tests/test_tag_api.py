from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Category
from blog.serializers import TagSerializer, CategorySerializer


TAG_URL = reverse('blog:tag-list')
CATEGORY_URL = reverse('blog:category-list')


def sample_tag(user, name='news'):
    """Create and return sample tag"""
    return Tag.objects.create(user=user, name=name)


def detail_url_tag(tag_id):
    """return tag detail url"""
    return reverse('blog:tag-detail', args=[tag_id])


def sample_category(user, name='computer'):
    """Create and return sample category"""
    return Category.objects.create(user=user, name=name)


def detail_url_category(category_id):
    """return category detail url"""
    return reverse('blog:category-detail', args=[category_id])


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


class PublicCategoryApiTest(TestCase):
    """Test Category object in Public mode"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving categories"""
        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryApiTest(TestCase):
    """Test the authorized user categories api"""

    def setUp(self):
        self.user = get_user_model().objects.create_staffuser(
            email='test@gmail.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_categories(self):
        """Test retrieving categories"""
        Category.objects.create(user=self.user, name='finance')
        Category.objects.create(user=self.user, name='computer')

        res = self.client.get(CATEGORY_URL)

        categories = Category.objects.all().order_by('-name')
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_category_successful(self):
        """Test creating a new category"""
        payload = {'user': self.user, 'name': 'laptop'}
        res = self.client.post(CATEGORY_URL, payload)

        exists = Category.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_update_category_successful(self):
        """Test updating one row data"""
        category = sample_category(self.user, name='computer')

        payload = {'user': self.user, 'name': 'architect'}
        res = self.client.put(detail_url_category(category.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        exists = Category.objects.filter(name='architect').exists()
        self.assertTrue(exists)

    def test_delete_category_successful(self):
        """Test deleting one row data"""
        category = sample_category(self.user, name='computer')
        res = self.client.delete(detail_url_category(category.id))
        exists = Category.objects.filter(name='computer').exists()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)

    def test_duplicate_category_fail(self):
        """Fail to creating duplicate category"""
        name = 'computer'
        sample_category(self.user, name=name)

        res = self.client.post(
            CATEGORY_URL,
            {'user': self.user, 'name': 'Computer'}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
