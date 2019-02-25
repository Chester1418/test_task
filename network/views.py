from django.shortcuts import render
from .serializers import SignUpSerializer, PostSerializer
from .models import Post
# Create your views here.
from django.contrib.auth.models import User
from rest_framework.views import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from . import hunter


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request, *args, **kwargs):
    serializer = SignUpSerializer(data=request.data)
    ehunter_response = hunter.email_verifier(request.data.get("email"))
    if ehunter_response['result'] == 'undeliverable':
        return Response('Email does not exist!',
                        status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        User.objects.create_user(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        request.data.update({"author": request.user.pk})
        return super(PostViewSet, self).create(request, *args, **kwargs)

    # Simple logic, just increment like/unlike.
    # User could like it`s own post, could like post more than once.
    @action(methods=['GET'], detail=True)
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        post.like += 1
        post.save()
        return Response({'message': f'Post with id: {post.id} liked'}, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def unlike(self, request, *args, **kwargs):
        post = self.get_object()
        post.unlike += 1
        post.save()
        return Response({'message': f'Post with id: {post.id} unliked'}, status=status.HTTP_201_CREATED)
