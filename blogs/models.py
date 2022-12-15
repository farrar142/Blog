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
    user_id = models.PositiveIntegerField()
    categories: models.Manager["Category"]


class Category(TitleBaseModel):
    objects = CategoryManager()
    user_id = models.PositiveIntegerField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="categories")
    order = models.PositiveIntegerField(default=0)


class Article(TitleBaseModel):
    user_id = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="articles"
    )
    content = models.TextField()


class Comment(CommonModel):
    user_id = models.PositiveIntegerField()
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    parent_comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="childs", null=True
    )
    content = models.TextField()
