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

__config__ = pulumi.Config('sdm')


class _ExportableConfig(types.ModuleType):
    @property
    def api_access_key(self) -> Optional[str]:
        """
        A GUID identifying the API key used to authenticate with the StrongDM API.
        """
        return __config__.get('apiAccessKey')

    @property
    def api_secret_key(self) -> Optional[str]:
        """
        A base64 encoded secret key used to authenticate with the StrongDM API.
        """
        return __config__.get('apiSecretKey')

    @property
    def host(self) -> Optional[str]:
        """
        The host and port of the StrongDM API endpoint.
        """
        return __config__.get('host')

    @property
    def retry_rate_limit_errors(self) -> Optional[bool]:
        """
        Whether experienced rate limits should cause the client to sleep instead of erroring out
        """
        return __config__.get_bool('retryRateLimitErrors')

