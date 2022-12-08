from typing import Literal, TypedDict, Any
from io import BytesIO
from typing import Literal, Optional, TypedDict
from calendar import timegm
from datetime import datetime

from django.utils.timezone import is_naive, make_aware, utc
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

from django.utils.datastructures import MultiValueDict
from django.http.request import HttpRequest
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http.request import QueryDict, HttpRequest
from rest_framework.request import Request


class Token(TypedDict):
    token_type: Literal["refresh"]
    exp: str
    iat: int
    jti: str
    user_id: int
    role: list[Literal["staff", "creator"]]


class MockRequest(HttpRequest, Request):
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE", "__default__"]
    user: Token | Literal[False]
    data: MultiValueDict[str, Any]
    FILES: MultiValueDict[str, InMemoryUploadedFile]
    query_params: QueryDict


def make_utc(dt):
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=utc)

    return dt


def aware_utcnow():
    return make_utc(datetime.utcnow())


def datetime_to_epoch(dt):
    return timegm(dt.utctimetuple())


def datetime_from_epoch(ts):
    return make_utc(datetime.utcfromtimestamp(ts))


def get_tags(validated_data: dict) -> list[str]:
    """
    >>> data = {"tags",["San,Two"]}
    """
    popped: list[str] = validated_data.pop("tags", None)
    if popped == None:
        return []
    if isinstance(popped, str):
        return popped.split(",")
    empty: list[str] = []
    for text in popped:
        if len(text.split(",")) >= 2:
            [empty.append(t) for t in text.split(",")]
        else:
            empty.append(text)
    return empty
