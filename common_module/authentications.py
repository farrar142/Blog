import os
import jwt
from typing import Optional, TypedDict, Literal
from django.http import HttpRequest
from ninja import errors
from ninja.security.http import HttpBearer
from rest_framework import authentication, exceptions
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from common_module.utils import Token, aware_utcnow, datetime_from_epoch

from dotenv import load_dotenv

load_dotenv()


def get_jwt_token_from_dict(data: dict):
    bearer_token: Optional[str] = data.get("HTTP_AUTHORIZATION")
    if not bearer_token:
        return False
    token = parse_bearer_token(bearer_token)
    if token:
        return token
    return False


def parse_bearer_token(token: str):
    splitted = token.split(" ")
    if not len(splitted) == 2:
        return False
    if splitted[0] != "Bearer":
        return False
    return splitted[1]


def parse_jwt(access_token: str):
    try:
        token = jwt.decode(access_token, options={"verify_signature": False})
        return Token(**token)
    except:
        return False


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def check_exp(self, payload: Token, claim="exp", current_time=None):
        if current_time is None:
            current_time = aware_utcnow()
        try:
            claim_value = payload[claim]
        except:
            raise exceptions.NotAuthenticated
        claim_time = datetime_from_epoch(claim_value)
        if claim_time <= current_time:
            raise exceptions.NotAuthenticated

    def authenticate(self, request: HttpRequest):
        jwt = get_jwt_token_from_dict(request.META)
        if not jwt:
            return (None, None)
        parsed = parse_jwt(jwt)
        if not parsed:
            return (None, None)
        self.check_exp(parsed)
        return (parsed, None)

    # def authenticate(self, request):
    #     print("errrrrorr")
    #     header = self.get_header(request)
    #     if header is None:
    #         return None

    #     raw_token = self.get_raw_token(header)
    #     if raw_token is None:
    #         return None
    #     return parse_jwt(raw_token)  # type: ignore


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str):
        info = parse_jwt(token)
        if info:
            return info
        raise errors.AuthenticationError
