from typing import Optional, TypedDict
import functools
from rest_framework import serializers, exceptions

from .utils import MockRequest
from .models import Image


class Context(TypedDict):
    request: Optional[MockRequest]


class BaseSerializer(serializers.ModelSerializer):
    context: Context

    @property
    def request(self):
        req = self.context.get("request")
        if req == None:
            raise exceptions.NotAcceptable(
                detail={"server": ["시리얼라이저에 리퀘스트가 할당되지 않았습니다"]}
            )
        return req

    @property
    def user(self):
        token = self.request.user
        return token


class ImageSerializer(BaseSerializer):
    class Meta:
        model = Image
        fields = ("url", "path")


def OnlyOneImageInjector(func):
    @functools.wraps(func)
    def wrapper(self: BaseSerializer, *args):
        validated_data = args[-1]
        image = validated_data.pop("image", None)
        if not self.user:
            raise exceptions.PermissionDenied
        user_id = self.user.get("user_id")
        if func.__name__ == "create":
            instance = func(self, validated_data)
        else:
            obj = args[0]
            instance = func(self, obj, validated_data)

        if image:
            Image.create_single_instance(user_id, instance, image)
        return instance

    return wrapper


def ImageAppendInjector(func):
    @functools.wraps(func)
    def wrapper(self: BaseSerializer, *args):
        validated_data = args[-1]
        image = validated_data.pop("image", None)
        if not self.user:
            raise exceptions.PermissionDenied
        user_id = self.user.get("user_id")
        if func.__name__ == "create":
            instance = func(self, validated_data)
        else:
            obj = args[0]
            instance = func(self, obj, validated_data)

        if image:
            Image.create_image(user_id, instance, image)
        return instance

    return wrapper


def UserIdInjector(func):
    @functools.wraps(func)
    def wrapper(*args):
        serializer: BaseSerializer = args[0]
        user = serializer.user
        validated_data: dict = args[-1]
        if not user:
            raise exceptions.PermissionDenied
        validated_data.update(user_id=user.get("user_id"))
        result = func(*args)
        return result

    return wrapper
