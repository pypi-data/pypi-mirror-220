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
    'GetServerResult',
    'AwaitableGetServerResult',
    'get_server',
    'get_server_output',
]

@pulumi.output_type
class GetServerResult:
    """
    A collection of values returned by getServer.
    """
    def __init__(__self__, arn=None, certificate=None, domain=None, endpoint=None, endpoint_type=None, id=None, identity_provider_type=None, invocation_role=None, logging_role=None, protocols=None, security_policy_name=None, server_id=None, url=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if certificate and not isinstance(certificate, str):
            raise TypeError("Expected argument 'certificate' to be a str")
        pulumi.set(__self__, "certificate", certificate)
        if domain and not isinstance(domain, str):
            raise TypeError("Expected argument 'domain' to be a str")
        pulumi.set(__self__, "domain", domain)
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, "endpoint", endpoint)
        if endpoint_type and not isinstance(endpoint_type, str):
            raise TypeError("Expected argument 'endpoint_type' to be a str")
        pulumi.set(__self__, "endpoint_type", endpoint_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity_provider_type and not isinstance(identity_provider_type, str):
            raise TypeError("Expected argument 'identity_provider_type' to be a str")
        pulumi.set(__self__, "identity_provider_type", identity_provider_type)
        if invocation_role and not isinstance(invocation_role, str):
            raise TypeError("Expected argument 'invocation_role' to be a str")
        pulumi.set(__self__, "invocation_role", invocation_role)
        if logging_role and not isinstance(logging_role, str):
            raise TypeError("Expected argument 'logging_role' to be a str")
        pulumi.set(__self__, "logging_role", logging_role)
        if protocols and not isinstance(protocols, list):
            raise TypeError("Expected argument 'protocols' to be a list")
        pulumi.set(__self__, "protocols", protocols)
        if security_policy_name and not isinstance(security_policy_name, str):
            raise TypeError("Expected argument 'security_policy_name' to be a str")
        pulumi.set(__self__, "security_policy_name", security_policy_name)
        if server_id and not isinstance(server_id, str):
            raise TypeError("Expected argument 'server_id' to be a str")
        pulumi.set(__self__, "server_id", server_id)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of Transfer Server.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def certificate(self) -> str:
        """
        ARN of any certificate.
        """
        return pulumi.get(self, "certificate")

    @property
    @pulumi.getter
    def domain(self) -> str:
        """
        The domain of the storage system that is used for file transfers.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter
    def endpoint(self) -> str:
        """
        Endpoint of the Transfer Server (e.g., `s-12345678.server.transfer.REGION.amazonaws.com`).
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of endpoint that the server is connected to.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="identityProviderType")
    def identity_provider_type(self) -> str:
        """
        The mode of authentication enabled for this service. The default value is `SERVICE_MANAGED`, which allows you to store and access SFTP user credentials within the service. `API_GATEWAY` indicates that user authentication requires a call to an API Gateway endpoint URL provided by you to integrate an identity provider of your choice.
        """
        return pulumi.get(self, "identity_provider_type")

    @property
    @pulumi.getter(name="invocationRole")
    def invocation_role(self) -> str:
        """
        ARN of the IAM role used to authenticate the user account with an `identity_provider_type` of `API_GATEWAY`.
        """
        return pulumi.get(self, "invocation_role")

    @property
    @pulumi.getter(name="loggingRole")
    def logging_role(self) -> str:
        """
        ARN of an IAM role that allows the service to write your SFTP users’ activity to your Amazon CloudWatch logs for monitoring and auditing purposes.
        """
        return pulumi.get(self, "logging_role")

    @property
    @pulumi.getter
    def protocols(self) -> Sequence[str]:
        """
        File transfer protocol or protocols over which your file transfer protocol client can connect to your server's endpoint.
        """
        return pulumi.get(self, "protocols")

    @property
    @pulumi.getter(name="securityPolicyName")
    def security_policy_name(self) -> str:
        """
        The name of the security policy that is attached to the server.
        """
        return pulumi.get(self, "security_policy_name")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> str:
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        URL of the service endpoint used to authenticate users with an `identity_provider_type` of `API_GATEWAY`.
        """
        return pulumi.get(self, "url")


class AwaitableGetServerResult(GetServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerResult(
            arn=self.arn,
            certificate=self.certificate,
            domain=self.domain,
            endpoint=self.endpoint,
            endpoint_type=self.endpoint_type,
            id=self.id,
            identity_provider_type=self.identity_provider_type,
            invocation_role=self.invocation_role,
            logging_role=self.logging_role,
            protocols=self.protocols,
            security_policy_name=self.security_policy_name,
            server_id=self.server_id,
            url=self.url)


def get_server(server_id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServerResult:
    """
    Use this data source to get the ARN of an AWS Transfer Server for use in other
    resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.transfer.get_server(server_id="s-1234567")
    ```


    :param str server_id: ID for an SFTP server.
    """
    __args__ = dict()
    __args__['serverId'] = server_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:transfer/getServer:getServer', __args__, opts=opts, typ=GetServerResult).value

    return AwaitableGetServerResult(
        arn=pulumi.get(__ret__, 'arn'),
        certificate=pulumi.get(__ret__, 'certificate'),
        domain=pulumi.get(__ret__, 'domain'),
        endpoint=pulumi.get(__ret__, 'endpoint'),
        endpoint_type=pulumi.get(__ret__, 'endpoint_type'),
        id=pulumi.get(__ret__, 'id'),
        identity_provider_type=pulumi.get(__ret__, 'identity_provider_type'),
        invocation_role=pulumi.get(__ret__, 'invocation_role'),
        logging_role=pulumi.get(__ret__, 'logging_role'),
        protocols=pulumi.get(__ret__, 'protocols'),
        security_policy_name=pulumi.get(__ret__, 'security_policy_name'),
        server_id=pulumi.get(__ret__, 'server_id'),
        url=pulumi.get(__ret__, 'url'))


@_utilities.lift_output_func(get_server)
def get_server_output(server_id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServerResult]:
    """
    Use this data source to get the ARN of an AWS Transfer Server for use in other
    resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.transfer.get_server(server_id="s-1234567")
    ```


    :param str server_id: ID for an SFTP server.
    """
    ...
