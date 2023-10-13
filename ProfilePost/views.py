
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
# from .permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters

class CommentListeCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        return CommentSerializer

class PostListeCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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

# class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
    
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         if instance:
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'Message': 'No Profile Found'}, status=status.HTTP_404_NOT_FOUND)


# def post_comment(request, instance, context):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             author = form.cleaned_data['author']
#             content = form.cleaned_data['content']

#             Comment.objects.create(content_object=instance, author=author, content=content)
           
#     else:
#         form = CommentForm()    
#     context['form'] = form


# def post(request):
#     post = get_object_or_404(Post)
#     comments = post.comments.all()

#     context = {
#         'post': post,
#         'comments': comments,
#     }
#     post_comment(request, post, context)
#     return render(request, 'post.html', context)


# def profile(request):
    # user = get_object_or_404(User)
    # profile = get_object_or_404(Profile, user=user)
   
    # comments = profile.comments.all()
    
    # context = {
    #     'user': user,
    #     'profile': profile,
    #     'comments': comments,
    # }
    # post_comment(request, profile, context)
    # return render(request, 'profile.html', context)