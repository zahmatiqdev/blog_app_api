from rest_framework import generics, authentication, permissions

from core.models import Tag
from .serializers import TagSerializer


class TagAPIView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagSerializer

    def get_queryset(self):
        request = self.request
        qs = Tag.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs
