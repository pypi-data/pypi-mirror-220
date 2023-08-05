# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetDistributionConfigurationsResult',
    'AwaitableGetDistributionConfigurationsResult',
    'get_distribution_configurations',
    'get_distribution_configurations_output',
]

@pulumi.output_type
class GetDistributionConfigurationsResult:
    """
    A collection of values returned by getDistributionConfigurations.
    """
    def __init__(__self__, arns=None, filters=None, id=None, names=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        pulumi.set(__self__, "arns", arns)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)

    @property
    @pulumi.getter
    def arns(self) -> Sequence[str]:
        """
        Set of ARNs of the matched Image Builder Distribution Configurations.
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetDistributionConfigurationsFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        Set of names of the matched Image Builder Distribution Configurations.
        """
        return pulumi.get(self, "names")


class AwaitableGetDistributionConfigurationsResult(GetDistributionConfigurationsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDistributionConfigurationsResult(
            arns=self.arns,
            filters=self.filters,
            id=self.id,
            names=self.names)


def get_distribution_configurations(filters: Optional[Sequence[pulumi.InputType['GetDistributionConfigurationsFilterArgs']]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDistributionConfigurationsResult:
    """
    Use this data source to get the ARNs and names of Image Builder Distribution Configurations matching the specified criteria.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.imagebuilder.get_distribution_configurations(filters=[aws.imagebuilder.GetDistributionConfigurationsFilterArgs(
        name="name",
        values=["example"],
    )])
    ```


    :param Sequence[pulumi.InputType['GetDistributionConfigurationsFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    """
    __args__ = dict()
    __args__['filters'] = filters
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:imagebuilder/getDistributionConfigurations:getDistributionConfigurations', __args__, opts=opts, typ=GetDistributionConfigurationsResult).value

    return AwaitableGetDistributionConfigurationsResult(
        arns=pulumi.get(__ret__, 'arns'),
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        names=pulumi.get(__ret__, 'names'))


@_utilities.lift_output_func(get_distribution_configurations)
def get_distribution_configurations_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetDistributionConfigurationsFilterArgs']]]]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDistributionConfigurationsResult]:
    """
    Use this data source to get the ARNs and names of Image Builder Distribution Configurations matching the specified criteria.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.imagebuilder.get_distribution_configurations(filters=[aws.imagebuilder.GetDistributionConfigurationsFilterArgs(
        name="name",
        values=["example"],
    )])
    ```


    :param Sequence[pulumi.InputType['GetDistributionConfigurationsFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    """
    ...
