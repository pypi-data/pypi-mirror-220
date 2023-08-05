# coding: utf-8
"""
    InductivaWebAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from inductiva.client import schemas  # noqa: F401


class User(schemas.DictSchema):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    class MetaOapg:
        required = {
            "email",
            "username",
        }

        class properties:
            username = schemas.StrSchema
            email = schemas.StrSchema
            is_active = schemas.BoolSchema
            is_admin = schemas.BoolSchema
            __annotations__ = {
                "username": username,
                "email": email,
                "is_active": is_active,
                "is_admin": is_admin,
            }

    email: MetaOapg.properties.email
    username: MetaOapg.properties.username

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["username"]
    ) -> MetaOapg.properties.username:
        ...

    @typing.overload
    def __getitem__(
            self, name: typing_extensions.Literal["email"]
    ) -> MetaOapg.properties.email:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["is_active"]
    ) -> MetaOapg.properties.is_active:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["is_admin"]
    ) -> MetaOapg.properties.is_admin:
        ...

    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema:
        ...

    def __getitem__(self, name: typing.Union[typing_extensions.Literal[
        "username",
        "email",
        "is_active",
        "is_admin",
    ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["username"]
    ) -> MetaOapg.properties.username:
        ...

    @typing.overload
    def get_item_oapg(
            self, name: typing_extensions.Literal["email"]
    ) -> MetaOapg.properties.email:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["is_active"]
    ) -> typing.Union[MetaOapg.properties.is_active, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["is_admin"]
    ) -> typing.Union[MetaOapg.properties.is_admin, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
            self, name: str
    ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]:
        ...

    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal[
        "username",
        "email",
        "is_active",
        "is_admin",
    ], str]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[
            dict,
            frozendict.frozendict,
        ],
        email: typing.Union[
            MetaOapg.properties.email,
            str,
        ],
        username: typing.Union[
            MetaOapg.properties.username,
            str,
        ],
        is_active: typing.Union[MetaOapg.properties.is_active, bool,
                                schemas.Unset] = schemas.unset,
        is_admin: typing.Union[MetaOapg.properties.is_admin, bool,
                               schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict,
                               frozendict.frozendict, str, date, datetime,
                               uuid.UUID, int, float, decimal.Decimal, None,
                               list, tuple, bytes],
    ) -> 'User':
        return super().__new__(
            cls,
            *_args,
            email=email,
            username=username,
            is_active=is_active,
            is_admin=is_admin,
            _configuration=_configuration,
            **kwargs,
        )
