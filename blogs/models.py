from django.db import models
from blogs.managers import BlogManager, CategoryManager
from users.models import User
from common_module.models import CommonModel


class TitleBaseModel(CommonModel):
    class Meta:
        abstract = True

    title = models.CharField(max_length=256)
    description = models.TextField(default="")


# Create your models here.
class Blog(TitleBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    objects = BlogManager()
    title = models.CharField(max_length=256, unique=True)
    categories: models.Manager["Category"]


class Category(TitleBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    objects = CategoryManager()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="categories")
    order = models.PositiveIntegerField(blank=True, default=0)
    title = models.CharField(max_length=256, default="")


class Article(TitleBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="articles"
    )
    is_saved = models.BooleanField(default=False)
    title = models.CharField(max_length=256, default="")
    content = models.TextField()


class Comment(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    parent_comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="childs", null=True
    )
    content = models.TextField()
