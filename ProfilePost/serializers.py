from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from .models import Post, Profile, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'content', 'content_type', 'object_id', 'content_object']

    def get_author_username(self, obj):
        return obj.author 

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['author', 'author_username', 'title', 'body', 'comments']

    def get_author_username(self, obj):
        return obj.author.username

    # def get_comments(self, obj):
    #     comments = Comment.objects.filter(content_type=obj)[:3]
    #     request = self.context.get('request')
    #     return {
    #         "comments": CommentSerializer(comments, many=True).data,
    #         "all_comment_link": request.build_absolute_uri(reverse('post_comment_list', kwargs={'object_id': obj.id}))
    #     }

class ProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'user_username', 'about', 'comments']

    def get_user_username(self, obj):
        return obj.user.username
