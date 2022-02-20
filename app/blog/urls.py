from django.urls import path

from . import views


app_name = 'blog'


urlpatterns = [
    path('tag/', views.TagAPIView.as_view(), name='tag-list'),

]
