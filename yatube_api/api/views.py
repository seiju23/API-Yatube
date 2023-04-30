from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, filters, generics
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post, Follow, User

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer, GroupSerializer,
    PostSerializer, FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Устанавливает автором поста по умолчанию текущего пользователя."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )

    def create_post(self):
        """Возвращает пост."""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post

    def get_queryset(self):
        """Возвращает комментарии для текущего поста."""
        comments = self.create_post().comments.all()
        return comments

    def perform_create(self, serializer):
        """Устанавливает автором по умолчанию текущего пользователя."""
        serializer.save(author=self.request.user, post=self.create_post())


class FollowView(generics.ListCreateAPIView):
    """Вью-класс для подписок."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', )

    def get_queryset(self):
        """Возвращает список подписок."""
        user = get_object_or_404(User, username=self.request.user)
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        """Устанавливает подписчиком текущего пользователя."""
        serializer.save(user=self.request.user)
