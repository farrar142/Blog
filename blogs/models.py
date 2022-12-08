from django.db import models
from blogs.managers import BlogManager, CategoryManager

from common_module.models import CommonModel


class TitleBaseModel(CommonModel):
    class Meta:
        abstract = True

    title = models.CharField(max_length=256)
    description = models.TextField(default="")


# Create your models here.
class Blog(TitleBaseModel):
    objects = BlogManager()
    categories: models.Manager["Category"]


class Category(TitleBaseModel):
    objects = CategoryManager()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="categories")
    order = models.PositiveIntegerField(default=0)


class Article(TitleBaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="articles"
    )
    content = models.TextField()


class Comment(CommonModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    parent_comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="childs", null=True
    )
    content = models.TextField()
