from django.shortcuts import get_object_or_404, render
import json

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from common_module import permissions
from blogs.serializers import (
    BlogReadOnlySerializer,
    BlogUpsertSerializer,
    CategoryReadOnlySerializer,
    CategoryUpsertSerializer,
)
from blogs.serializers import ArticleReadOnlySerializer, ArticleUpsertSerializer

from blogs.models import Article, Blog, Category
from common_module.views import DisallowEditOtherUsersResourceMixin
from .crawler import get_articles, Article as VArticle

# Create your views here.


class BlogViewSets(DisallowEditOtherUsersResourceMixin[Blog]):
    queryset = Blog.objects.all()
    filterset_fields = ("user__id", "user__nickname")
    # search_fields = ["tags__name"]
    ordering_fileds = ("created_at",)
    ordering = ("-created_at",)
    read_only_serializer = BlogReadOnlySerializer
    upsert_serializer = BlogUpsertSerializer

    @action(methods=["GET"], detail=False, url_path="nickname/(?P<nickname>[^/.]+)")
    def find_by_nickname(self, *args, **kwargs):
        nickname = kwargs.get("nickname")
        obj = get_object_or_404(Blog, user__nickname=nickname)
        serialzier = self.get_serializer(instance=obj)
        return Response(data=serialzier.data)


class CategoryViewSets(DisallowEditOtherUsersResourceMixin[Category]):
    queryset = Category.objects.all()
    filterset_fields = ("blog__title",)
    ordering_fileds = ("created_at",)
    ordering = ("-created_at",)
    read_only_serializer = CategoryReadOnlySerializer
    upsert_serializer = CategoryUpsertSerializer


class ArticleViewSets(DisallowEditOtherUsersResourceMixin[Article]):
    queryset = Article.objects.all()
    filterset_fields = ("blog", "category")
    # search_fields = ["tags__name"]
    ordering_fileds = ("created_at",)
    ordering = ("-created_at",)
    read_only_serializer = ArticleReadOnlySerializer
    upsert_serializer = ArticleUpsertSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(is_saved=True)
        return super().list(request, *args, **kwargs)


from ninja import NinjaAPI, Schema


api = NinjaAPI(csrf=False)


class VelogArticle(Schema):
    href: str
    headline: str
    context: str
    date: str
    tags: list[str]


@api.get("{username}")
def get_velog_articles(request, username: str):
    articles = get_articles(username)
    listdict = VArticle.list_to_dict(articles)
    return json.loads(json.dumps(listdict, ensure_ascii=False))


209 - 50 - 40

119 - 32

87
