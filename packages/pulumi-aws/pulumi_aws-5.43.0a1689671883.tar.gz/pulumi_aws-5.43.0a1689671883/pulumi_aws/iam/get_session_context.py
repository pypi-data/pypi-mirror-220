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
    'GetSessionContextResult',
    'AwaitableGetSessionContextResult',
    'get_session_context',
    'get_session_context_output',
]

@pulumi.output_type
class GetSessionContextResult:
    """
    A collection of values returned by getSessionContext.
    """
    def __init__(__self__, arn=None, id=None, issuer_arn=None, issuer_id=None, issuer_name=None, session_name=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if issuer_arn and not isinstance(issuer_arn, str):
            raise TypeError("Expected argument 'issuer_arn' to be a str")
        pulumi.set(__self__, "issuer_arn", issuer_arn)
        if issuer_id and not isinstance(issuer_id, str):
            raise TypeError("Expected argument 'issuer_id' to be a str")
        pulumi.set(__self__, "issuer_id", issuer_id)
        if issuer_name and not isinstance(issuer_name, str):
            raise TypeError("Expected argument 'issuer_name' to be a str")
        pulumi.set(__self__, "issuer_name", issuer_name)
        if session_name and not isinstance(session_name, str):
            raise TypeError("Expected argument 'session_name' to be a str")
        pulumi.set(__self__, "session_name", session_name)

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="issuerArn")
    def issuer_arn(self) -> str:
        """
        IAM source role ARN if `arn` corresponds to an STS assumed role. Otherwise, `issuer_arn` is equal to `arn`.
        """
        return pulumi.get(self, "issuer_arn")

    @property
    @pulumi.getter(name="issuerId")
    def issuer_id(self) -> str:
        """
        Unique identifier of the IAM role that issues the STS assumed role.
        """
        return pulumi.get(self, "issuer_id")

    @property
    @pulumi.getter(name="issuerName")
    def issuer_name(self) -> str:
        """
        Name of the source role. Only available if `arn` corresponds to an STS assumed role.
        """
        return pulumi.get(self, "issuer_name")

    @property
    @pulumi.getter(name="sessionName")
    def session_name(self) -> str:
        """
        Name of the STS session. Only available if `arn` corresponds to an STS assumed role.
        """
        return pulumi.get(self, "session_name")


class AwaitableGetSessionContextResult(GetSessionContextResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSessionContextResult(
            arn=self.arn,
            id=self.id,
            issuer_arn=self.issuer_arn,
            issuer_id=self.issuer_id,
            issuer_name=self.issuer_name,
            session_name=self.session_name)


def get_session_context(arn: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSessionContextResult:
    """
    This data source provides information on the IAM source role of an STS assumed role. For non-role ARNs, this data source simply passes the ARN through in `issuer_arn`.

    For some AWS resources, multiple types of principals are allowed in the same argument (e.g., IAM users and IAM roles). However, these arguments often do not allow assumed-role (i.e., STS, temporary credential) principals. Given an STS ARN, this data source provides the ARN for the source IAM role.

    ## Example Usage
    ### Basic Example

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.iam.get_session_context(arn="arn:aws:sts::123456789012:assumed-role/Audien-Heaven/MatyNoyes")
    ```
    ### Find the Provider's Source Role

    Combined with `get_caller_identity`, you can get the current user's source IAM role ARN (`issuer_arn`) if you're using an assumed role. If you're not using an assumed role, the caller's (e.g., an IAM user's) ARN will simply be passed through. In environments where both IAM users and individuals using assumed roles need to apply the same configurations, this data source enables seamless use.

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.get_caller_identity()
    example = aws.iam.get_session_context(arn=current.arn)
    ```


    :param str arn: ARN for an assumed role.
           
           > If `arn` is a non-role ARN, the provider gives no error and `issuer_arn` will be equal to the `arn` value. For STS assumed-role ARNs, the provider gives an error if the identified IAM role does not exist.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:iam/getSessionContext:getSessionContext', __args__, opts=opts, typ=GetSessionContextResult).value

    return AwaitableGetSessionContextResult(
        arn=pulumi.get(__ret__, 'arn'),
        id=pulumi.get(__ret__, 'id'),
        issuer_arn=pulumi.get(__ret__, 'issuer_arn'),
        issuer_id=pulumi.get(__ret__, 'issuer_id'),
        issuer_name=pulumi.get(__ret__, 'issuer_name'),
        session_name=pulumi.get(__ret__, 'session_name'))


@_utilities.lift_output_func(get_session_context)
def get_session_context_output(arn: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSessionContextResult]:
    """
    This data source provides information on the IAM source role of an STS assumed role. For non-role ARNs, this data source simply passes the ARN through in `issuer_arn`.

    For some AWS resources, multiple types of principals are allowed in the same argument (e.g., IAM users and IAM roles). However, these arguments often do not allow assumed-role (i.e., STS, temporary credential) principals. Given an STS ARN, this data source provides the ARN for the source IAM role.

    ## Example Usage
    ### Basic Example

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.iam.get_session_context(arn="arn:aws:sts::123456789012:assumed-role/Audien-Heaven/MatyNoyes")
    ```
    ### Find the Provider's Source Role

    Combined with `get_caller_identity`, you can get the current user's source IAM role ARN (`issuer_arn`) if you're using an assumed role. If you're not using an assumed role, the caller's (e.g., an IAM user's) ARN will simply be passed through. In environments where both IAM users and individuals using assumed roles need to apply the same configurations, this data source enables seamless use.

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.get_caller_identity()
    example = aws.iam.get_session_context(arn=current.arn)
    ```


    :param str arn: ARN for an assumed role.
           
           > If `arn` is a non-role ARN, the provider gives no error and `issuer_arn` will be equal to the `arn` value. For STS assumed-role ARNs, the provider gives an error if the identified IAM role does not exist.
    """
    ...
