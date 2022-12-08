from typing import TYPE_CHECKING, Optional
from django.db import models
from rest_framework import exceptions

if TYPE_CHECKING:
    from .models import Blog, Category


class CategoryManager(models.Manager):
    def create(self, **kwargs):
        blog: Optional[Blog] = kwargs.get("blog")
        if not blog:
            raise exceptions.NotAcceptable(
                detail={"server": ["카테고리 오브젝트는 blog_id가 아닌 Blog객체로 넘겨주세요"]}
            )
        category_before: Optional[Category] = (
            blog.categories.all().order_by("-order").last()
        )
        if category_before:
            kwargs.update(order=category_before.order + 1)
        return super().create(**kwargs)


class BlogManager(models.Manager):
    def create(self, **kwargs):
        user_id: Optional[int] = kwargs.get("user_id")
        if not user_id:
            raise exceptions.PermissionDenied(detail={"blog": ["로그인되지 않은 유저입니다"]})
        already = self.get_queryset().filter(user_id=user_id).first()
        if already:
            raise exceptions.ValidationError(detail={"blog": ["이미 블로그가 존재합니다."]})
        return super().create(**kwargs)
