# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetIpRangesResult',
    'AwaitableGetIpRangesResult',
    'get_ip_ranges',
    'get_ip_ranges_output',
]

@pulumi.output_type
class GetIpRangesResult:
    """
    A collection of values returned by getIpRanges.
    """
    def __init__(__self__, cidr_blocks=None, create_date=None, id=None, ipv6_cidr_blocks=None, regions=None, services=None, sync_token=None, url=None):
        if cidr_blocks and not isinstance(cidr_blocks, list):
            raise TypeError("Expected argument 'cidr_blocks' to be a list")
        pulumi.set(__self__, "cidr_blocks", cidr_blocks)
        if create_date and not isinstance(create_date, str):
            raise TypeError("Expected argument 'create_date' to be a str")
        pulumi.set(__self__, "create_date", create_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ipv6_cidr_blocks and not isinstance(ipv6_cidr_blocks, list):
            raise TypeError("Expected argument 'ipv6_cidr_blocks' to be a list")
        pulumi.set(__self__, "ipv6_cidr_blocks", ipv6_cidr_blocks)
        if regions and not isinstance(regions, list):
            raise TypeError("Expected argument 'regions' to be a list")
        pulumi.set(__self__, "regions", regions)
        if services and not isinstance(services, list):
            raise TypeError("Expected argument 'services' to be a list")
        pulumi.set(__self__, "services", services)
        if sync_token and not isinstance(sync_token, int):
            raise TypeError("Expected argument 'sync_token' to be a int")
        pulumi.set(__self__, "sync_token", sync_token)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter(name="cidrBlocks")
    def cidr_blocks(self) -> Sequence[str]:
        """
        Lexically ordered list of CIDR blocks.
        """
        return pulumi.get(self, "cidr_blocks")

    @property
    @pulumi.getter(name="createDate")
    def create_date(self) -> str:
        """
        Publication time of the IP ranges (e.g., `2016-08-03-23-46-05`).
        """
        return pulumi.get(self, "create_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipv6CidrBlocks")
    def ipv6_cidr_blocks(self) -> Sequence[str]:
        """
        Lexically ordered list of IPv6 CIDR blocks.
        """
        return pulumi.get(self, "ipv6_cidr_blocks")

    @property
    @pulumi.getter
    def regions(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "regions")

    @property
    @pulumi.getter
    def services(self) -> Sequence[str]:
        return pulumi.get(self, "services")

    @property
    @pulumi.getter(name="syncToken")
    def sync_token(self) -> int:
        """
        Publication time of the IP ranges, in Unix epoch time format
        (e.g., `1470267965`).
        """
        return pulumi.get(self, "sync_token")

    @property
    @pulumi.getter
    def url(self) -> Optional[str]:
        return pulumi.get(self, "url")


class AwaitableGetIpRangesResult(GetIpRangesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIpRangesResult(
            cidr_blocks=self.cidr_blocks,
            create_date=self.create_date,
            id=self.id,
            ipv6_cidr_blocks=self.ipv6_cidr_blocks,
            regions=self.regions,
            services=self.services,
            sync_token=self.sync_token,
            url=self.url)


def get_ip_ranges(regions: Optional[Sequence[str]] = None,
                  services: Optional[Sequence[str]] = None,
                  url: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIpRangesResult:
    """
    Use this data source to get the IP ranges of various AWS products and services. For more information about the contents of this data source and required JSON syntax if referencing a custom URL, see the [AWS IP Address Ranges documentation](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    european_ec2 = aws.get_ip_ranges(regions=[
            "eu-west-1",
            "eu-central-1",
        ],
        services=["ec2"])
    from_europe = aws.ec2.SecurityGroup("fromEurope",
        ingress=[aws.ec2.SecurityGroupIngressArgs(
            from_port=443,
            to_port=443,
            protocol="tcp",
            cidr_blocks=european_ec2.cidr_blocks,
            ipv6_cidr_blocks=european_ec2.ipv6_cidr_blocks,
        )],
        tags={
            "CreateDate": european_ec2.create_date,
            "SyncToken": european_ec2.sync_token,
        })
    ```


    :param Sequence[str] regions: Filter IP ranges by regions (or include all regions, if
           omitted). Valid items are `global` (for `cloudfront`) as well as all AWS regions
           (e.g., `eu-central-1`)
    :param Sequence[str] services: Filter IP ranges by services. Valid items are `amazon`
           (for amazon.com), `amazon_connect`, `api_gateway`, `cloud9`, `cloudfront`,
           `codebuild`, `dynamodb`, `ec2`, `ec2_instance_connect`, `globalaccelerator`,
           `route53`, `route53_healthchecks`, `s3` and `workspaces_gateways`. See the
           [`service` attribute][2] documentation for other possible values.
           
           > **NOTE:** If the specified combination of regions and services does not yield any
           CIDR blocks, this call will fail.
    :param str url: Custom URL for source JSON file. Syntax must match [AWS IP Address Ranges documentation](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html). Defaults to `https://ip-ranges.amazonaws.com/ip-ranges.json`.
    """
    __args__ = dict()
    __args__['regions'] = regions
    __args__['services'] = services
    __args__['url'] = url
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:index/getIpRanges:getIpRanges', __args__, opts=opts, typ=GetIpRangesResult).value

    return AwaitableGetIpRangesResult(
        cidr_blocks=pulumi.get(__ret__, 'cidr_blocks'),
        create_date=pulumi.get(__ret__, 'create_date'),
        id=pulumi.get(__ret__, 'id'),
        ipv6_cidr_blocks=pulumi.get(__ret__, 'ipv6_cidr_blocks'),
        regions=pulumi.get(__ret__, 'regions'),
        services=pulumi.get(__ret__, 'services'),
        sync_token=pulumi.get(__ret__, 'sync_token'),
        url=pulumi.get(__ret__, 'url'))


@_utilities.lift_output_func(get_ip_ranges)
def get_ip_ranges_output(regions: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                         services: Optional[pulumi.Input[Sequence[str]]] = None,
                         url: Optional[pulumi.Input[Optional[str]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIpRangesResult]:
    """
    Use this data source to get the IP ranges of various AWS products and services. For more information about the contents of this data source and required JSON syntax if referencing a custom URL, see the [AWS IP Address Ranges documentation](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    european_ec2 = aws.get_ip_ranges(regions=[
            "eu-west-1",
            "eu-central-1",
        ],
        services=["ec2"])
    from_europe = aws.ec2.SecurityGroup("fromEurope",
        ingress=[aws.ec2.SecurityGroupIngressArgs(
            from_port=443,
            to_port=443,
            protocol="tcp",
            cidr_blocks=european_ec2.cidr_blocks,
            ipv6_cidr_blocks=european_ec2.ipv6_cidr_blocks,
        )],
        tags={
            "CreateDate": european_ec2.create_date,
            "SyncToken": european_ec2.sync_token,
        })
    ```


    :param Sequence[str] regions: Filter IP ranges by regions (or include all regions, if
           omitted). Valid items are `global` (for `cloudfront`) as well as all AWS regions
           (e.g., `eu-central-1`)
    :param Sequence[str] services: Filter IP ranges by services. Valid items are `amazon`
           (for amazon.com), `amazon_connect`, `api_gateway`, `cloud9`, `cloudfront`,
           `codebuild`, `dynamodb`, `ec2`, `ec2_instance_connect`, `globalaccelerator`,
           `route53`, `route53_healthchecks`, `s3` and `workspaces_gateways`. See the
           [`service` attribute][2] documentation for other possible values.
           
           > **NOTE:** If the specified combination of regions and services does not yield any
           CIDR blocks, this call will fail.
    :param str url: Custom URL for source JSON file. Syntax must match [AWS IP Address Ranges documentation](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html). Defaults to `https://ip-ranges.amazonaws.com/ip-ranges.json`.
    """
    ...
