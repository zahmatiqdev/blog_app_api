from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='testuser@gmail.com', password='testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'amtz1311@gmail.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'amtz@gMAil.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises errpr"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = 'test@gmail.com'
        password = 'test123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_new_staffuser(self):
        """Test creating a new staff user"""
        email = 'teststaff@gmail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_staffuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)

    def test_create_new_tag(self):
        """Tag to be used for a blog"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='news'
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_new_category(self):
        """Category to be used for a blog"""
        category = models.Category.objects.create(
            user=sample_user(),
            name='Programming'
        )

        self.assertEqual(str(category), category.name)

    def test_create_new_post(self):
        """Post to be used for a blog"""
        post = models.Post.objects.create(
            user=sample_user(),
            title='Programming',
        )

        self.assertEqual(str(post), post.title)

    @patch('uuid.uuid4')
    def test_blog_file_with_uuid_name(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.blog_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/blog/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
