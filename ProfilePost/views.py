from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Post, Comment, Profile
from .serializers import CommentSerializer, PostSerializer, ProfileSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class CommentListeCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            object_id = self.kwargs.get('object_id')
            model_name = self.kwargs.get('model_name')
            content_type = None

            if model_name == 'post':
                model_class = Post
            elif model_name == 'profile':
                model_class = Profile
            else:
                # Handle other models if necessary
                return Comment.objects.none()

            content_type = ContentType.objects.get_for_model(model_class)
            return Comment.objects.filter(content_type=content_type, object_id=object_id, author=self.request.user)
        else:
            return Comment.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            object_id = self.kwargs.get('object_id')
            model_name = self.kwargs.get('model_name')
            content_type = None

            if model_name == 'post':
                model_class = Post
            elif model_name == 'profile':
                model_class = Profile
            else:
                # Handle other models if necessary
                raise serializers.ValidationError({'Message': 'Invalid model_name'})

            content_type = ContentType.objects.get_for_model(model_class)

            if Comment.objects.filter(content_type=content_type, object_id=object_id).exists():
                raise serializers.ValidationError({'Message': 'You have already added a comment.'})

            serializer.save(author=self.request.user, content_type=content_type, object_id=object_id)
        else:
            # Handle the case when the user is not authenticated
            raise serializers.ValidationError({'Message': 'Authentication is required to add a comment.'})

    def get_serializer_class(self):
        return CommentSerializer

class PostListeCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer(queryset, many=True)

    def get_serializer_class(self):
        return PostSerializer

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'No Post Found'}, status=status.HTTP_404_NOT_FOUND)

class ProfileListeCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_serializer_class(self):
        return ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'No Profile Found'}, status=status.HTTP_404_NOT_FOUND)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        
        content_type_model = comment.content_type.model_class()
        object_id = comment.object_id

        related_object = get_object_or_404(content_type_model, id=object_id)

        if related_object.author != self.request.user:
            raise serializers.ValidationError({"Message": "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)

        return comment

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()

        return super().delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        comment = self.get_object()

        return super().put(request, *args, **kwargs)
    
