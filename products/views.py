from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from .models import Product, Comment, Like
from .serializers import *
from .paginator import CustomPagination



class ProductListView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        products = Product.objects.all()
        page = self.pagination_class()
        page = page.paginate_queryset(products, request)
        serializer = ProductSerializer(page, many=True)
        return page.response(serializer.data)


class ProductCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)




class ProductUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product.owner != request.user:
            raise ValidationError("Siz bu mahsulotni o'zgartira olmaysiz.")
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get(self, request, product_id):
        comments = Comment.objects.filter(product_id=product_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def delete(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        if comment.user != request.user:
            raise ValidationError("Siz bu kommentni o'chira olmaysiz.")
        comment.delete()
        return Response(status=204)


class LikeCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        product_id = Product.objects.get(pk=pk)
        like , created = Like.objects.get_or_create(product_id=product_id, user=request.user)
        if not created:
            product_id.likes_count -= 1
            product_id.save(update_fields=["likes_count"])
            like.delete()
        else:
            product_id.likes_count += 1
            product_id.save(update_fields=["likes_count"])
        return Response(status=201)










