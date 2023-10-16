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
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['author', 'content', 'content_type', 'object_id', 'content_object']

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj.content_object).model
    
    def get_content_object(self, obj):
        return str(obj.content_object)


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['author', 'author_username', 'title', 'body', 'comments']

    def get_comments(self, obj):
        # Query comments based on the Post instance's primary key
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk)
        request = self.context.get('request')
       
        all_comment_link = request.build_absolute_uri(reverse('comment_list', kwargs={'model_name': 'post', 'object_id': obj.pk}))
        return {
            "comments": CommentSerializer(comments, many=True).data,
            "all_comment_link": all_comment_link
        }

class ProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'user_username', 'about', 'comments']

    def get_comments(self, obj):
        # Query comments based on the Post instance's primary key
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk)
        request = self.context.get('request')
        all_comment_link = request.build_absolute_uri(reverse('comment_list', kwargs={'model_name': 'profile', 'object_id': obj.pk}))
        return {
            "comments": CommentSerializer(comments, many=True).data,
            "all_comment_link": all_comment_link
        }

