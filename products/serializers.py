from rest_framework import serializers
from .models import Comment, Product



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'owner', 'price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']


    def create(self, validated_data):
        request = self.context.get('request')
        return Product.objects.create(owner=request.user, **validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['owner'] = {
            'id': instance.owner.id,
            'username': instance.owner.username,
            'email': instance.owner.email,
        }
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'product', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        return Comment.objects.create(user=request.user, **validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = {
            'id': instance.user.id,
            'username': instance.user.username,
            'email': instance.user.email,
        }
        return data
    





    