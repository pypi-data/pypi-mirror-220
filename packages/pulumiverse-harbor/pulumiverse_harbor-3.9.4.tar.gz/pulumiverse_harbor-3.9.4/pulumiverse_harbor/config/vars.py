# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

import types

__config__ = pulumi.Config('harbor')


class _ExportableConfig(types.ModuleType):
    @property
    def api_version(self) -> Optional[int]:
        return __config__.get_int('apiVersion')

    @property
    def insecure(self) -> Optional[bool]:
        return __config__.get_bool('insecure')

    @property
    def password(self) -> Optional[str]:
        return __config__.get('password')

    @property
    def url(self) -> Optional[str]:
        return __config__.get('url')

    @property
    def username(self) -> Optional[str]:
        return __config__.get('username')

