from django.urls import path

from . import views


app_name = 'blog'


urlpatterns = [
    path('tag/', views.TagAPIView.as_view(), name='tag-list'),
    path('tag/<int:pk>/', views.TagDetailAPIView.as_view(), name='tag-detail'),
    path('category/', views.CategoryAPIView.as_view(), name='category-list'),
    path('category/<int:pk>/',
         views.CategoryDetailAPIView.as_view(),
         name='category-detail'),
    path('post/', views.PostAPIView.as_view(), name='post-list'),
    path('post/<str:slug>/',
         views.PostDetailAPIView.as_view(),
         name='post-detail-slug'),
]
