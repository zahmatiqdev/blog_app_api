from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category
from blog.serializers import CategorySerializer


CATEGORY_URL = reverse('blog:category-list')


def sample_category(user, name='computer'):
    """Create and return sample category"""
    return Category.objects.create(user=user, name=name)


def detail_url_category(category_id):
    """return category detail url"""
    return reverse('blog:category-detail', args=[category_id])


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
