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
    'GetFunctionsResult',
    'AwaitableGetFunctionsResult',
    'get_functions',
]

@pulumi.output_type
class GetFunctionsResult:
    """
    A collection of values returned by getFunctions.
    """
    def __init__(__self__, function_arns=None, function_names=None, id=None):
        if function_arns and not isinstance(function_arns, list):
            raise TypeError("Expected argument 'function_arns' to be a list")
        pulumi.set(__self__, "function_arns", function_arns)
        if function_names and not isinstance(function_names, list):
            raise TypeError("Expected argument 'function_names' to be a list")
        pulumi.set(__self__, "function_names", function_names)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="functionArns")
    def function_arns(self) -> Sequence[str]:
        """
        A list of Lambda Function ARNs.
        """
        return pulumi.get(self, "function_arns")

    @property
    @pulumi.getter(name="functionNames")
    def function_names(self) -> Sequence[str]:
        """
        A list of Lambda Function names.
        """
        return pulumi.get(self, "function_names")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetFunctionsResult(GetFunctionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFunctionsResult(
            function_arns=self.function_arns,
            function_names=self.function_names,
            id=self.id)


def get_functions(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFunctionsResult:
    """
    Data resource to get a list of Lambda Functions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    all = aws.lambda.get_functions()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:lambda/getFunctions:getFunctions', __args__, opts=opts, typ=GetFunctionsResult).value

    return AwaitableGetFunctionsResult(
        function_arns=pulumi.get(__ret__, 'function_arns'),
        function_names=pulumi.get(__ret__, 'function_names'),
        id=pulumi.get(__ret__, 'id'))
