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

__all__ = [
    'EndpointAccessVpcEndpoint',
    'EndpointAccessVpcEndpointNetworkInterface',
    'WorkgroupConfigParameter',
    'WorkgroupEndpoint',
    'WorkgroupEndpointVpcEndpoint',
    'WorkgroupEndpointVpcEndpointNetworkInterface',
    'GetWorkgroupEndpointResult',
    'GetWorkgroupEndpointVpcEndpointResult',
    'GetWorkgroupEndpointVpcEndpointNetworkInterfaceResult',
]

@pulumi.output_type
class EndpointAccessVpcEndpoint(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "networkInterfaces":
            suggest = "network_interfaces"
        elif key == "vpcEndpointId":
            suggest = "vpc_endpoint_id"
        elif key == "vpcId":
            suggest = "vpc_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointAccessVpcEndpoint. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointAccessVpcEndpoint.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointAccessVpcEndpoint.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 network_interfaces: Optional[Sequence['outputs.EndpointAccessVpcEndpointNetworkInterface']] = None,
                 vpc_endpoint_id: Optional[str] = None,
                 vpc_id: Optional[str] = None):
        """
        :param Sequence['EndpointAccessVpcEndpointNetworkInterfaceArgs'] network_interfaces: The network interfaces of the endpoint.. See `Network Interface` below.
        :param str vpc_endpoint_id: The DNS address of the VPC endpoint.
        :param str vpc_id: The port that Amazon Redshift Serverless listens on.
        """
        if network_interfaces is not None:
            pulumi.set(__self__, "network_interfaces", network_interfaces)
        if vpc_endpoint_id is not None:
            pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[Sequence['outputs.EndpointAccessVpcEndpointNetworkInterface']]:
        """
        The network interfaces of the endpoint.. See `Network Interface` below.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> Optional[str]:
        """
        The DNS address of the VPC endpoint.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        The port that Amazon Redshift Serverless listens on.
        """
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class EndpointAccessVpcEndpointNetworkInterface(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "availabilityZone":
            suggest = "availability_zone"
        elif key == "networkInterfaceId":
            suggest = "network_interface_id"
        elif key == "privateIpAddress":
            suggest = "private_ip_address"
        elif key == "subnetId":
            suggest = "subnet_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointAccessVpcEndpointNetworkInterface. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointAccessVpcEndpointNetworkInterface.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointAccessVpcEndpointNetworkInterface.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 availability_zone: Optional[str] = None,
                 network_interface_id: Optional[str] = None,
                 private_ip_address: Optional[str] = None,
                 subnet_id: Optional[str] = None):
        """
        :param str availability_zone: The availability Zone.
        :param str network_interface_id: The unique identifier of the network interface.
        :param str private_ip_address: The IPv4 address of the network interface within the subnet.
        :param str subnet_id: The unique identifier of the subnet.
        """
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        The availability Zone.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[str]:
        """
        The unique identifier of the network interface.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[str]:
        """
        The IPv4 address of the network interface within the subnet.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[str]:
        """
        The unique identifier of the subnet.
        """
        return pulumi.get(self, "subnet_id")


@pulumi.output_type
class WorkgroupConfigParameter(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "parameterKey":
            suggest = "parameter_key"
        elif key == "parameterValue":
            suggest = "parameter_value"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkgroupConfigParameter. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkgroupConfigParameter.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkgroupConfigParameter.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 parameter_key: str,
                 parameter_value: str):
        """
        :param str parameter_key: The key of the parameter. The options are `datestyle`, `enable_user_activity_logging`, `query_group`, `search_path`, and `max_query_execution_time`.
        :param str parameter_value: The value of the parameter to set.
        """
        pulumi.set(__self__, "parameter_key", parameter_key)
        pulumi.set(__self__, "parameter_value", parameter_value)

    @property
    @pulumi.getter(name="parameterKey")
    def parameter_key(self) -> str:
        """
        The key of the parameter. The options are `datestyle`, `enable_user_activity_logging`, `query_group`, `search_path`, and `max_query_execution_time`.
        """
        return pulumi.get(self, "parameter_key")

    @property
    @pulumi.getter(name="parameterValue")
    def parameter_value(self) -> str:
        """
        The value of the parameter to set.
        """
        return pulumi.get(self, "parameter_value")


@pulumi.output_type
class WorkgroupEndpoint(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "vpcEndpoints":
            suggest = "vpc_endpoints"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkgroupEndpoint. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkgroupEndpoint.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkgroupEndpoint.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 address: Optional[str] = None,
                 port: Optional[int] = None,
                 vpc_endpoints: Optional[Sequence['outputs.WorkgroupEndpointVpcEndpoint']] = None):
        """
        :param str address: The DNS address of the VPC endpoint.
        :param int port: The port that Amazon Redshift Serverless listens on.
        :param Sequence['WorkgroupEndpointVpcEndpointArgs'] vpc_endpoints: The VPC endpoint or the Redshift Serverless workgroup. See `VPC Endpoint` below.
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if vpc_endpoints is not None:
            pulumi.set(__self__, "vpc_endpoints", vpc_endpoints)

    @property
    @pulumi.getter
    def address(self) -> Optional[str]:
        """
        The DNS address of the VPC endpoint.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        The port that Amazon Redshift Serverless listens on.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="vpcEndpoints")
    def vpc_endpoints(self) -> Optional[Sequence['outputs.WorkgroupEndpointVpcEndpoint']]:
        """
        The VPC endpoint or the Redshift Serverless workgroup. See `VPC Endpoint` below.
        """
        return pulumi.get(self, "vpc_endpoints")


@pulumi.output_type
class WorkgroupEndpointVpcEndpoint(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "networkInterfaces":
            suggest = "network_interfaces"
        elif key == "vpcEndpointId":
            suggest = "vpc_endpoint_id"
        elif key == "vpcId":
            suggest = "vpc_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkgroupEndpointVpcEndpoint. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkgroupEndpointVpcEndpoint.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkgroupEndpointVpcEndpoint.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 network_interfaces: Optional[Sequence['outputs.WorkgroupEndpointVpcEndpointNetworkInterface']] = None,
                 vpc_endpoint_id: Optional[str] = None,
                 vpc_id: Optional[str] = None):
        """
        :param Sequence['WorkgroupEndpointVpcEndpointNetworkInterfaceArgs'] network_interfaces: The network interfaces of the endpoint.. See `Network Interface` below.
        :param str vpc_endpoint_id: The DNS address of the VPC endpoint.
        :param str vpc_id: The port that Amazon Redshift Serverless listens on.
        """
        if network_interfaces is not None:
            pulumi.set(__self__, "network_interfaces", network_interfaces)
        if vpc_endpoint_id is not None:
            pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[Sequence['outputs.WorkgroupEndpointVpcEndpointNetworkInterface']]:
        """
        The network interfaces of the endpoint.. See `Network Interface` below.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> Optional[str]:
        """
        The DNS address of the VPC endpoint.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        The port that Amazon Redshift Serverless listens on.
        """
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class WorkgroupEndpointVpcEndpointNetworkInterface(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "availabilityZone":
            suggest = "availability_zone"
        elif key == "networkInterfaceId":
            suggest = "network_interface_id"
        elif key == "privateIpAddress":
            suggest = "private_ip_address"
        elif key == "subnetId":
            suggest = "subnet_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkgroupEndpointVpcEndpointNetworkInterface. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkgroupEndpointVpcEndpointNetworkInterface.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkgroupEndpointVpcEndpointNetworkInterface.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 availability_zone: Optional[str] = None,
                 network_interface_id: Optional[str] = None,
                 private_ip_address: Optional[str] = None,
                 subnet_id: Optional[str] = None):
        """
        :param str availability_zone: The availability Zone.
        :param str network_interface_id: The unique identifier of the network interface.
        :param str private_ip_address: The IPv4 address of the network interface within the subnet.
        :param str subnet_id: The unique identifier of the subnet.
        """
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        The availability Zone.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[str]:
        """
        The unique identifier of the network interface.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[str]:
        """
        The IPv4 address of the network interface within the subnet.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[str]:
        """
        The unique identifier of the subnet.
        """
        return pulumi.get(self, "subnet_id")


@pulumi.output_type
class GetWorkgroupEndpointResult(dict):
    def __init__(__self__, *,
                 address: str,
                 port: int,
                 vpc_endpoints: Sequence['outputs.GetWorkgroupEndpointVpcEndpointResult']):
        """
        :param str address: The DNS address of the VPC endpoint.
        :param int port: The port that Amazon Redshift Serverless listens on.
        :param Sequence['GetWorkgroupEndpointVpcEndpointArgs'] vpc_endpoints: The VPC endpoint or the Redshift Serverless workgroup. See `VPC Endpoint` below.
        """
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "port", port)
        pulumi.set(__self__, "vpc_endpoints", vpc_endpoints)

    @property
    @pulumi.getter
    def address(self) -> str:
        """
        The DNS address of the VPC endpoint.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port that Amazon Redshift Serverless listens on.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="vpcEndpoints")
    def vpc_endpoints(self) -> Sequence['outputs.GetWorkgroupEndpointVpcEndpointResult']:
        """
        The VPC endpoint or the Redshift Serverless workgroup. See `VPC Endpoint` below.
        """
        return pulumi.get(self, "vpc_endpoints")


@pulumi.output_type
class GetWorkgroupEndpointVpcEndpointResult(dict):
    def __init__(__self__, *,
                 network_interfaces: Sequence['outputs.GetWorkgroupEndpointVpcEndpointNetworkInterfaceResult'],
                 vpc_endpoint_id: str,
                 vpc_id: str):
        """
        :param Sequence['GetWorkgroupEndpointVpcEndpointNetworkInterfaceArgs'] network_interfaces: The network interfaces of the endpoint.. See `Network Interface` below.
        :param str vpc_endpoint_id: The DNS address of the VPC endpoint.
        :param str vpc_id: The port that Amazon Redshift Serverless listens on.
        """
        pulumi.set(__self__, "network_interfaces", network_interfaces)
        pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Sequence['outputs.GetWorkgroupEndpointVpcEndpointNetworkInterfaceResult']:
        """
        The network interfaces of the endpoint.. See `Network Interface` below.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> str:
        """
        The DNS address of the VPC endpoint.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        The port that Amazon Redshift Serverless listens on.
        """
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class GetWorkgroupEndpointVpcEndpointNetworkInterfaceResult(dict):
    def __init__(__self__, *,
                 availability_zone: str,
                 network_interface_id: str,
                 private_ip_address: str,
                 subnet_id: str):
        """
        :param str availability_zone: The availability Zone.
        :param str network_interface_id: The unique identifier of the network interface.
        :param str private_ip_address: The IPv4 address of the network interface within the subnet.
        :param str subnet_id: The unique identifier of the subnet.
        """
        pulumi.set(__self__, "availability_zone", availability_zone)
        pulumi.set(__self__, "network_interface_id", network_interface_id)
        pulumi.set(__self__, "private_ip_address", private_ip_address)
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> str:
        """
        The availability Zone.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> str:
        """
        The unique identifier of the network interface.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> str:
        """
        The IPv4 address of the network interface within the subnet.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        """
        The unique identifier of the subnet.
        """
        return pulumi.get(self, "subnet_id")


