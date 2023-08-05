# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetAuthorizationTokenResult',
    'AwaitableGetAuthorizationTokenResult',
    'get_authorization_token',
    'get_authorization_token_output',
]

@pulumi.output_type
class GetAuthorizationTokenResult:
    """
    A collection of values returned by getAuthorizationToken.
    """
    def __init__(__self__, authorization_token=None, domain=None, domain_owner=None, duration_seconds=None, expiration=None, id=None):
        if authorization_token and not isinstance(authorization_token, str):
            raise TypeError("Expected argument 'authorization_token' to be a str")
        pulumi.set(__self__, "authorization_token", authorization_token)
        if domain and not isinstance(domain, str):
            raise TypeError("Expected argument 'domain' to be a str")
        pulumi.set(__self__, "domain", domain)
        if domain_owner and not isinstance(domain_owner, str):
            raise TypeError("Expected argument 'domain_owner' to be a str")
        pulumi.set(__self__, "domain_owner", domain_owner)
        if duration_seconds and not isinstance(duration_seconds, int):
            raise TypeError("Expected argument 'duration_seconds' to be a int")
        pulumi.set(__self__, "duration_seconds", duration_seconds)
        if expiration and not isinstance(expiration, str):
            raise TypeError("Expected argument 'expiration' to be a str")
        pulumi.set(__self__, "expiration", expiration)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="authorizationToken")
    def authorization_token(self) -> str:
        """
        Temporary authorization token.
        """
        return pulumi.get(self, "authorization_token")

    @property
    @pulumi.getter
    def domain(self) -> str:
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="domainOwner")
    def domain_owner(self) -> str:
        return pulumi.get(self, "domain_owner")

    @property
    @pulumi.getter(name="durationSeconds")
    def duration_seconds(self) -> Optional[int]:
        return pulumi.get(self, "duration_seconds")

    @property
    @pulumi.getter
    def expiration(self) -> str:
        """
        Time in UTC RFC3339 format when the authorization token expires.
        """
        return pulumi.get(self, "expiration")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetAuthorizationTokenResult(GetAuthorizationTokenResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAuthorizationTokenResult(
            authorization_token=self.authorization_token,
            domain=self.domain,
            domain_owner=self.domain_owner,
            duration_seconds=self.duration_seconds,
            expiration=self.expiration,
            id=self.id)


def get_authorization_token(domain: Optional[str] = None,
                            domain_owner: Optional[str] = None,
                            duration_seconds: Optional[int] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAuthorizationTokenResult:
    """
    The CodeArtifact Authorization Token data source generates a temporary authentication token for accessing repositories in a CodeArtifact domain.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.codeartifact.get_authorization_token(domain=aws_codeartifact_domain["test"]["domain"])
    ```


    :param str domain: Name of the domain that is in scope for the generated authorization token.
    :param str domain_owner: Account number of the AWS account that owns the domain.
    :param int duration_seconds: Time, in seconds, that the generated authorization token is valid. Valid values are `0` and between `900` and `43200`.
    """
    __args__ = dict()
    __args__['domain'] = domain
    __args__['domainOwner'] = domain_owner
    __args__['durationSeconds'] = duration_seconds
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:codeartifact/getAuthorizationToken:getAuthorizationToken', __args__, opts=opts, typ=GetAuthorizationTokenResult).value

    return AwaitableGetAuthorizationTokenResult(
        authorization_token=pulumi.get(__ret__, 'authorization_token'),
        domain=pulumi.get(__ret__, 'domain'),
        domain_owner=pulumi.get(__ret__, 'domain_owner'),
        duration_seconds=pulumi.get(__ret__, 'duration_seconds'),
        expiration=pulumi.get(__ret__, 'expiration'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_authorization_token)
def get_authorization_token_output(domain: Optional[pulumi.Input[str]] = None,
                                   domain_owner: Optional[pulumi.Input[Optional[str]]] = None,
                                   duration_seconds: Optional[pulumi.Input[Optional[int]]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAuthorizationTokenResult]:
    """
    The CodeArtifact Authorization Token data source generates a temporary authentication token for accessing repositories in a CodeArtifact domain.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.codeartifact.get_authorization_token(domain=aws_codeartifact_domain["test"]["domain"])
    ```


    :param str domain: Name of the domain that is in scope for the generated authorization token.
    :param str domain_owner: Account number of the AWS account that owns the domain.
    :param int duration_seconds: Time, in seconds, that the generated authorization token is valid. Valid values are `0` and between `900` and `43200`.
    """
    ...
