from django.urls import path
from .views import *



urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:product_id>/', CommentCreateView.as_view(), name='comment-list'),
    path('comments/<int:comment_id>/delete/', CommentCreateView.as_view(), name='comment-delete'),
    path('products/<int:pk>/like/', LikeCreateView.as_view(), name='like-create'),
]