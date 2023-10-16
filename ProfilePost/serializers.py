from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from .models import Post, Profile, Comment
from django.urls import reverse

class CommentSerializer(serializers.ModelSerializer):
    object_id = serializers.StringRelatedField(read_only=True)
    content_type = serializers.SerializerMethodField()
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['content', 'content_type', 'object_id', 'content_object']

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj.content_object).model
    
    def get_content_object(self, obj):
        return str(obj.content_object)

class BaseSerializerWithComments(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk)
        request = self.context.get('request')
        return {
            "comments": CommentSerializer(comments, many=True).data,
            "all_comment_link": request.build_absolute_uri(reverse('comment_list', kwargs={'object_id': obj.pk}))
        }

class PostSerializer(BaseSerializerWithComments):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['author', 'author_username', 'title', 'body', 'comments']

class ProfileSerializer(BaseSerializerWithComments):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['user', 'user_username', 'about', 'comments']

