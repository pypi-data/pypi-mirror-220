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


class TaskRequest(schemas.DictSchema):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    class MetaOapg:
        required = {
            "method",
            "params",
        }

        class properties:
            method = schemas.StrSchema
            params = schemas.DictSchema

            class resource_pool(
                    schemas.ComposedSchema,):

                class MetaOapg:
                    format = 'uuid4'
                    any_of_0 = schemas.StrSchema
                    any_of_1 = schemas.NoneSchema

                    @classmethod
                    @functools.lru_cache()
                    def any_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            cls.any_of_0,
                            cls.any_of_1,
                        ]

                def __new__(
                    cls,
                    *_args: typing.Union[
                        dict,
                        frozendict.frozendict,
                        str,
                        date,
                        datetime,
                        uuid.UUID,
                        int,
                        float,
                        decimal.Decimal,
                        bool,
                        None,
                        list,
                        tuple,
                        bytes,
                        io.FileIO,
                        io.BufferedReader,
                    ],
                    _configuration: typing.Optional[
                        schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict,
                                           frozendict.frozendict, str, date,
                                           datetime, uuid.UUID, int, float,
                                           decimal.Decimal, None, list, tuple,
                                           bytes],
                ) -> 'resource_pool':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )

            __annotations__ = {
                "method": method,
                "params": params,
                "resource_pool": resource_pool,
            }

    method: MetaOapg.properties.method
    params: MetaOapg.properties.params

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["method"]
    ) -> MetaOapg.properties.method:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["params"]
    ) -> MetaOapg.properties.params:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["resource_pool"]
    ) -> MetaOapg.properties.resource_pool:
        ...

    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema:
        ...

    def __getitem__(self, name: typing.Union[typing_extensions.Literal[
        "method",
        "params",
        "resource_pool",
    ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["method"]
    ) -> MetaOapg.properties.method:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["params"]
    ) -> MetaOapg.properties.params:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["resource_pool"]
    ) -> typing.Union[MetaOapg.properties.resource_pool, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
            self, name: str
    ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]:
        ...

    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal[
        "method",
        "params",
        "resource_pool",
    ], str]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[
            dict,
            frozendict.frozendict,
        ],
        method: typing.Union[
            MetaOapg.properties.method,
            str,
        ],
        params: typing.Union[
            MetaOapg.properties.params,
            dict,
            frozendict.frozendict,
        ],
        resource_pool: typing.Union[MetaOapg.properties.resource_pool, dict,
                                    frozendict.frozendict, str, date, datetime,
                                    uuid.UUID, int, float, decimal.Decimal,
                                    bool, None, list, tuple, bytes, io.FileIO,
                                    io.BufferedReader,
                                    schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict,
                               frozendict.frozendict, str, date, datetime,
                               uuid.UUID, int, float, decimal.Decimal, None,
                               list, tuple, bytes],
    ) -> 'TaskRequest':
        return super().__new__(
            cls,
            *_args,
            method=method,
            params=params,
            resource_pool=resource_pool,
            _configuration=_configuration,
            **kwargs,
        )
