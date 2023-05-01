from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post, Follow

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
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Устанавливает автором поста по умолчанию текущего пользователя."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


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
        return self.create_post().comments.all()

    def perform_create(self, serializer):
        """Устанавливает автором по умолчанию текущего пользователя."""
        serializer.save(author=self.request.user, post=self.create_post())


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet
                    ):
    """Вью-класс для подписок."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', )

    def get_queryset(self):
        """Возвращает список подписок."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Устанавливает подписчиком текущего пользователя."""
        serializer.save(user=self.request.user)
