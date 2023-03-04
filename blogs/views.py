from django.shortcuts import render
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
    filterset_fields = ("user_id",)
    # search_fields = ["tags__name"]
    ordering_fileds = ("created_at",)
    ordering = ("-created_at",)

    def get_serializer_class(self):
        serializer_classes = {
            "GET": BlogReadOnlySerializer,
            "__default__": BlogUpsertSerializer,
        }
        method = self.request.method or "GET"

        return serializer_classes.get(method, serializer_classes.get("__default__"))

    # @action(methods=["GET"], detail=False, url_path="find_by_name/")
    # def get_blog_of_user(self, *args, **kwargs):
    #     return Response({})


class CategoryViewSets(DisallowEditOtherUsersResourceMixin[Category]):
    queryset = Category.objects.all()
    filterset_fields = ("blog__title",)
    ordering_fileds = ("created_at",)
    ordering = ("-created_at",)

    def get_serializer_class(self):
        serializer_classes = {
            "GET": CategoryReadOnlySerializer,
            "__default__": CategoryUpsertSerializer,
        }
        method = self.request.method or "GET"

        return serializer_classes.get(method, serializer_classes.get("__default__"))


class ArticleViewSets(DisallowEditOtherUsersResourceMixin[Article]):
    queryset = Article.objects.all()
    filterset_fields = ("blog", "category")
    # search_fields = ["tags__name"]
    ordering_fileds = ("created_at",)
    ordering = ("-created_at",)

    def get_serializer_class(self):
        serializer_classes = {
            "GET": ArticleReadOnlySerializer,
            "__default__": ArticleUpsertSerializer,
        }
        method = self.request.method or "GET"

        return serializer_classes.get(method, serializer_classes.get("__default__"))

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
