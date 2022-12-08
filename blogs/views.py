from django.shortcuts import render

from rest_framework import viewsets
from blogs.serializers import BlogReadOnlySerializer, BlogUpsertSerializer

from blogs.models import Blog

# Create your views here.


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    # filterset_fields = []
    # search_fields = ["tags__name"]
    ordering_fileds = ["created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        serializer_classes = {
            "GET": BlogReadOnlySerializer,
            "__default__": BlogUpsertSerializer,
        }
        method = self.request.method or "GET"

        return serializer_classes.get(method, serializer_classes.get("__default__"))
