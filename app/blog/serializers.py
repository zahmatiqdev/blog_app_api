from rest_framework import serializers

from core.models import Tag, Category, Post


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_field = ('id',)
        ordering = ('-name',)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category object"""

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_field = ('id',)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post object"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'tags', 'categories', 'title',
                  'subtitle', 'slug', 'body', 'meta_description',
                  'date_created', 'date_modified', 'publish_date',
                  'published', 'image'
                  )
        read_only_field = (
            'id', 'date_created', 'date_modified',
            'published', 'publish_date',
        )
