from django.shortcuts import render

from rest_framework import viewsets
from blogs.serializers import (
    BlogReadOnlySerializer,
    BlogUpsertSerializer,
    CategoryReadOnlySerializer,
    CategoryUpsertSerializer,
)
from blogs.serializers import ArticleReadOnlySerializer, ArticleUpsertSerializer

from blogs.models import Article, Blog, Category

# Create your views here.


class BlogViewSets(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    # filterset_fields = []
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


class CategoryViewSets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filterset_fields = ("blog",)
    # search_fields = ["tags__name"]
    ordering_fileds = ("created_at",)
    ordering = ("-created_at",)

    def get_serializer_class(self):
        serializer_classes = {
            "GET": CategoryReadOnlySerializer,
            "__default__": CategoryUpsertSerializer,
        }
        method = self.request.method or "GET"

        return serializer_classes.get(method, serializer_classes.get("__default__"))


class ArticleViewSets(viewsets.ModelViewSet):
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
