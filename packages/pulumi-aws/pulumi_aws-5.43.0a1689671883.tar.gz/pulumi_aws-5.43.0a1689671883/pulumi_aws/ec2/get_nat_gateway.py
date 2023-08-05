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
    'GetNatGatewayResult',
    'AwaitableGetNatGatewayResult',
    'get_nat_gateway',
    'get_nat_gateway_output',
]

@pulumi.output_type
class GetNatGatewayResult:
    """
    A collection of values returned by getNatGateway.
    """
    def __init__(__self__, allocation_id=None, association_id=None, connectivity_type=None, filters=None, id=None, network_interface_id=None, private_ip=None, public_ip=None, state=None, subnet_id=None, tags=None, vpc_id=None):
        if allocation_id and not isinstance(allocation_id, str):
            raise TypeError("Expected argument 'allocation_id' to be a str")
        pulumi.set(__self__, "allocation_id", allocation_id)
        if association_id and not isinstance(association_id, str):
            raise TypeError("Expected argument 'association_id' to be a str")
        pulumi.set(__self__, "association_id", association_id)
        if connectivity_type and not isinstance(connectivity_type, str):
            raise TypeError("Expected argument 'connectivity_type' to be a str")
        pulumi.set(__self__, "connectivity_type", connectivity_type)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if network_interface_id and not isinstance(network_interface_id, str):
            raise TypeError("Expected argument 'network_interface_id' to be a str")
        pulumi.set(__self__, "network_interface_id", network_interface_id)
        if private_ip and not isinstance(private_ip, str):
            raise TypeError("Expected argument 'private_ip' to be a str")
        pulumi.set(__self__, "private_ip", private_ip)
        if public_ip and not isinstance(public_ip, str):
            raise TypeError("Expected argument 'public_ip' to be a str")
        pulumi.set(__self__, "public_ip", public_ip)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="allocationId")
    def allocation_id(self) -> str:
        """
        ID of the EIP allocated to the selected Nat Gateway.
        """
        return pulumi.get(self, "allocation_id")

    @property
    @pulumi.getter(name="associationId")
    def association_id(self) -> str:
        """
        The association ID of the Elastic IP address that's associated with the NAT gateway. Only available when `connectivity_type` is `public`.
        """
        return pulumi.get(self, "association_id")

    @property
    @pulumi.getter(name="connectivityType")
    def connectivity_type(self) -> str:
        """
        Connectivity type of the NAT Gateway.
        """
        return pulumi.get(self, "connectivity_type")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetNatGatewayFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> str:
        """
        The ID of the ENI allocated to the selected Nat Gateway.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter(name="privateIp")
    def private_ip(self) -> str:
        """
        Private Ip address of the selected Nat Gateway.
        """
        return pulumi.get(self, "private_ip")

    @property
    @pulumi.getter(name="publicIp")
    def public_ip(self) -> str:
        """
        Public Ip (EIP) address of the selected Nat Gateway.
        """
        return pulumi.get(self, "public_ip")

    @property
    @pulumi.getter
    def state(self) -> str:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        return pulumi.get(self, "vpc_id")


class AwaitableGetNatGatewayResult(GetNatGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNatGatewayResult(
            allocation_id=self.allocation_id,
            association_id=self.association_id,
            connectivity_type=self.connectivity_type,
            filters=self.filters,
            id=self.id,
            network_interface_id=self.network_interface_id,
            private_ip=self.private_ip,
            public_ip=self.public_ip,
            state=self.state,
            subnet_id=self.subnet_id,
            tags=self.tags,
            vpc_id=self.vpc_id)


def get_nat_gateway(filters: Optional[Sequence[pulumi.InputType['GetNatGatewayFilterArgs']]] = None,
                    id: Optional[str] = None,
                    state: Optional[str] = None,
                    subnet_id: Optional[str] = None,
                    tags: Optional[Mapping[str, str]] = None,
                    vpc_id: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNatGatewayResult:
    """
    Provides details about a specific Nat Gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    default = aws.ec2.get_nat_gateway(subnet_id=aws_subnet["public"]["id"])
    ```

    Usage with tags:

    ```python
    import pulumi
    import pulumi_aws as aws

    default = aws.ec2.get_nat_gateway(subnet_id=aws_subnet["public"]["id"],
        tags={
            "Name": "gw NAT",
        })
    ```


    :param Sequence[pulumi.InputType['GetNatGatewayFilterArgs']] filters: Custom filter block as described below.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    :param str id: ID of the specific Nat Gateway to retrieve.
    :param str state: State of the NAT gateway (pending | failed | available | deleting | deleted ).
    :param str subnet_id: ID of subnet that the Nat Gateway resides in.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired Nat Gateway.
    :param str vpc_id: ID of the VPC that the Nat Gateway resides in.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['id'] = id
    __args__['state'] = state
    __args__['subnetId'] = subnet_id
    __args__['tags'] = tags
    __args__['vpcId'] = vpc_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getNatGateway:getNatGateway', __args__, opts=opts, typ=GetNatGatewayResult).value

    return AwaitableGetNatGatewayResult(
        allocation_id=pulumi.get(__ret__, 'allocation_id'),
        association_id=pulumi.get(__ret__, 'association_id'),
        connectivity_type=pulumi.get(__ret__, 'connectivity_type'),
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        network_interface_id=pulumi.get(__ret__, 'network_interface_id'),
        private_ip=pulumi.get(__ret__, 'private_ip'),
        public_ip=pulumi.get(__ret__, 'public_ip'),
        state=pulumi.get(__ret__, 'state'),
        subnet_id=pulumi.get(__ret__, 'subnet_id'),
        tags=pulumi.get(__ret__, 'tags'),
        vpc_id=pulumi.get(__ret__, 'vpc_id'))


@_utilities.lift_output_func(get_nat_gateway)
def get_nat_gateway_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetNatGatewayFilterArgs']]]]] = None,
                           id: Optional[pulumi.Input[Optional[str]]] = None,
                           state: Optional[pulumi.Input[Optional[str]]] = None,
                           subnet_id: Optional[pulumi.Input[Optional[str]]] = None,
                           tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                           vpc_id: Optional[pulumi.Input[Optional[str]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNatGatewayResult]:
    """
    Provides details about a specific Nat Gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    default = aws.ec2.get_nat_gateway(subnet_id=aws_subnet["public"]["id"])
    ```

    Usage with tags:

    ```python
    import pulumi
    import pulumi_aws as aws

    default = aws.ec2.get_nat_gateway(subnet_id=aws_subnet["public"]["id"],
        tags={
            "Name": "gw NAT",
        })
    ```


    :param Sequence[pulumi.InputType['GetNatGatewayFilterArgs']] filters: Custom filter block as described below.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    :param str id: ID of the specific Nat Gateway to retrieve.
    :param str state: State of the NAT gateway (pending | failed | available | deleting | deleted ).
    :param str subnet_id: ID of subnet that the Nat Gateway resides in.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired Nat Gateway.
    :param str vpc_id: ID of the VPC that the Nat Gateway resides in.
    """
    ...
