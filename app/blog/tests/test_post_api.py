from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post
from blog.serializers import PostSerializer


POST_URL = reverse('blog:post-list')


def sample_post(user, **params):
    """Create and return sample post"""
    payload = {
        'title': 'the sample title',
        'slug': 'the-sample-title'
    }
    payload.update(params)
    return Post.objects.create(user=user, **payload)


def detail_url_with_slug(post_slug):
    """Return post detail URL with slug"""
    return reverse('blog:post-detail-slug', args=[post_slug])


def detail_url_with_date(post_date):
    """return post detail URL with date"""
    return reverse('blog:post-detail-date', args=[post_date])


class PublicPostApiTests(TestCase):
    """Test unauthenticated post API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTests(TestCase):
    """Test unauthenticated post API access"""

    def setUp(self):
        self.user = get_user_model().objects.create_staffuser(
            email='test@gmail.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_posts(self):
        """Test retrieving posts"""
        Post.objects.create(
            user=self.user,
            title='feedback',
            slug='this-is-feedback'
        )
        Post.objects.create(
            user=self.user,
            title='community',
            slug='this-is-community'
        )

        res = self.client.get(POST_URL)

        posts = Post.objects.all().order_by('-publish_date')
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_post_successful(self):
        """Test creating a new post"""
        payload = {
            'user': self.user,
            'title': 'This is Test title',
            'slug': 'This-is-test-title',
        }
        res = self.client.post(POST_URL, payload)

        exists = Post.objects.filter(
            user=self.user,
            title=payload['title']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_retrieve_post_with_slug(self):
        """Test retrieving a post with slug data"""
        post = Post.objects.create(
            user=self.user,
            title='feedback',
            slug='this-is-feedback'
        )
        url = detail_url_with_slug(post.slug)

        res = self.client.get(url)

        serializer = PostSerializer(post)
        self.assertEqual(res.data, serializer.data)
