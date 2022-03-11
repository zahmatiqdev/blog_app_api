from rest_framework import generics, mixins, authentication, permissions

from core.models import Tag, Category, Post
from .serializers import TagSerializer, CategorySerializer, PostSerializer


class TagAPIView(generics.CreateAPIView, generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    serializer_class = TagSerializer

    def get_queryset(self):
        request = self.request
        qs = Tag.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagDetailAPIView(mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       generics.RetrieveAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryAPIView(generics.CreateAPIView, generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    serializer_class = CategorySerializer

    def get_queryset(self):
        request = self.request
        qs = Category.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetailAPIView(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            generics.RetrieveAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostAPIView(generics.CreateAPIView, generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    serializer_class = PostSerializer

    def get_queryset(self):
        request = self.request
        qs = Post.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        generics.RetrieveAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
