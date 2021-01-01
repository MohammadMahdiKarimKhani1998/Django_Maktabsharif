from django.contrib.auth import get_user_model
from rest_framework import serializers
from blog.models import Post, Category

User = get_user_model()


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128)
    slug = serializers.SlugField(max_length=20)
    content = serializers.CharField(allow_null=True)
    draft = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    publish_time = serializers.DateTimeField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    # def validate_slug(self, slug):
    #     pass

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.content = validated_data.get('content', instance.content)
        instance.draft = validated_data.get('draft', instance.draft)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.publish_time = validated_data.get('publish_time', instance.publish_time)
        instance.save()
        return instance
