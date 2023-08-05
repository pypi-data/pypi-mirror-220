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
    'ClusterCacheNode',
    'ClusterLogDeliveryConfiguration',
    'GlobalReplicationGroupGlobalNodeGroup',
    'ParameterGroupParameter',
    'ReplicationGroupClusterMode',
    'ReplicationGroupLogDeliveryConfiguration',
    'UserAuthenticationMode',
    'GetClusterCacheNodeResult',
    'GetClusterLogDeliveryConfigurationResult',
    'GetReplicationGroupLogDeliveryConfigurationResult',
    'GetUserAuthenticationModeResult',
]

@pulumi.output_type
class ClusterCacheNode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "availabilityZone":
            suggest = "availability_zone"
        elif key == "outpostArn":
            suggest = "outpost_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterCacheNode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterCacheNode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterCacheNode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 address: Optional[str] = None,
                 availability_zone: Optional[str] = None,
                 id: Optional[str] = None,
                 outpost_arn: Optional[str] = None,
                 port: Optional[int] = None):
        """
        :param str availability_zone: Availability Zone for the cache cluster. If you want to create cache nodes in multi-az, use `preferred_availability_zones` instead. Default: System chosen Availability Zone. Changing this value will re-create the resource.
        :param int port: The port number on which each of the cache nodes will accept connections. For Memcached the default is 11211, and for Redis the default port is 6379. Cannot be provided with `replication_group_id`. Changing this value will re-create the resource.
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if outpost_arn is not None:
            pulumi.set(__self__, "outpost_arn", outpost_arn)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def address(self) -> Optional[str]:
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        Availability Zone for the cache cluster. If you want to create cache nodes in multi-az, use `preferred_availability_zones` instead. Default: System chosen Availability Zone. Changing this value will re-create the resource.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> Optional[str]:
        return pulumi.get(self, "outpost_arn")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        The port number on which each of the cache nodes will accept connections. For Memcached the default is 11211, and for Redis the default port is 6379. Cannot be provided with `replication_group_id`. Changing this value will re-create the resource.
        """
        return pulumi.get(self, "port")


@pulumi.output_type
class ClusterLogDeliveryConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "destinationType":
            suggest = "destination_type"
        elif key == "logFormat":
            suggest = "log_format"
        elif key == "logType":
            suggest = "log_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterLogDeliveryConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterLogDeliveryConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterLogDeliveryConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 destination: str,
                 destination_type: str,
                 log_format: str,
                 log_type: str):
        """
        :param str destination: Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        :param str destination_type: For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        :param str log_format: Valid values are `json` or `text`
        :param str log_type: Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter
    def destination(self) -> str:
        """
        Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> str:
        """
        For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        """
        return pulumi.get(self, "destination_type")

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> str:
        """
        Valid values are `json` or `text`
        """
        return pulumi.get(self, "log_format")

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        """
        Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        return pulumi.get(self, "log_type")


@pulumi.output_type
class GlobalReplicationGroupGlobalNodeGroup(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "globalNodeGroupId":
            suggest = "global_node_group_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GlobalReplicationGroupGlobalNodeGroup. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GlobalReplicationGroupGlobalNodeGroup.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GlobalReplicationGroupGlobalNodeGroup.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 global_node_group_id: Optional[str] = None,
                 slots: Optional[str] = None):
        """
        :param str global_node_group_id: The ID of the global node group.
        :param str slots: The keyspace for this node group.
        """
        if global_node_group_id is not None:
            pulumi.set(__self__, "global_node_group_id", global_node_group_id)
        if slots is not None:
            pulumi.set(__self__, "slots", slots)

    @property
    @pulumi.getter(name="globalNodeGroupId")
    def global_node_group_id(self) -> Optional[str]:
        """
        The ID of the global node group.
        """
        return pulumi.get(self, "global_node_group_id")

    @property
    @pulumi.getter
    def slots(self) -> Optional[str]:
        """
        The keyspace for this node group.
        """
        return pulumi.get(self, "slots")


@pulumi.output_type
class ParameterGroupParameter(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        :param str name: The name of the ElastiCache parameter.
        :param str value: The value of the ElastiCache parameter.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the ElastiCache parameter.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the ElastiCache parameter.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ReplicationGroupClusterMode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "numNodeGroups":
            suggest = "num_node_groups"
        elif key == "replicasPerNodeGroup":
            suggest = "replicas_per_node_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationGroupClusterMode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationGroupClusterMode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ReplicationGroupClusterMode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 num_node_groups: Optional[int] = None,
                 replicas_per_node_group: Optional[int] = None):
        """
        :param int num_node_groups: Number of node groups (shards) for this Redis replication group. Changing this number will trigger an online resizing operation before other settings modifications. Required unless `global_replication_group_id` is set.
        :param int replicas_per_node_group: Number of replica nodes in each node group. Valid values are 0 to 5. Changing this number will trigger an online resizing operation before other settings modifications.
        """
        if num_node_groups is not None:
            pulumi.set(__self__, "num_node_groups", num_node_groups)
        if replicas_per_node_group is not None:
            pulumi.set(__self__, "replicas_per_node_group", replicas_per_node_group)

    @property
    @pulumi.getter(name="numNodeGroups")
    def num_node_groups(self) -> Optional[int]:
        """
        Number of node groups (shards) for this Redis replication group. Changing this number will trigger an online resizing operation before other settings modifications. Required unless `global_replication_group_id` is set.
        """
        warnings.warn("""Use root-level num_node_groups instead""", DeprecationWarning)
        pulumi.log.warn("""num_node_groups is deprecated: Use root-level num_node_groups instead""")

        return pulumi.get(self, "num_node_groups")

    @property
    @pulumi.getter(name="replicasPerNodeGroup")
    def replicas_per_node_group(self) -> Optional[int]:
        """
        Number of replica nodes in each node group. Valid values are 0 to 5. Changing this number will trigger an online resizing operation before other settings modifications.
        """
        warnings.warn("""Use root-level replicas_per_node_group instead""", DeprecationWarning)
        pulumi.log.warn("""replicas_per_node_group is deprecated: Use root-level replicas_per_node_group instead""")

        return pulumi.get(self, "replicas_per_node_group")


@pulumi.output_type
class ReplicationGroupLogDeliveryConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "destinationType":
            suggest = "destination_type"
        elif key == "logFormat":
            suggest = "log_format"
        elif key == "logType":
            suggest = "log_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationGroupLogDeliveryConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationGroupLogDeliveryConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ReplicationGroupLogDeliveryConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 destination: str,
                 destination_type: str,
                 log_format: str,
                 log_type: str):
        """
        :param str destination: Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        :param str destination_type: For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        :param str log_format: Valid values are `json` or `text`
        :param str log_type: Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter
    def destination(self) -> str:
        """
        Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> str:
        """
        For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        """
        return pulumi.get(self, "destination_type")

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> str:
        """
        Valid values are `json` or `text`
        """
        return pulumi.get(self, "log_format")

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        """
        Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        return pulumi.get(self, "log_type")


@pulumi.output_type
class UserAuthenticationMode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "passwordCount":
            suggest = "password_count"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserAuthenticationMode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserAuthenticationMode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UserAuthenticationMode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type: str,
                 password_count: Optional[int] = None,
                 passwords: Optional[Sequence[str]] = None):
        """
        :param str type: Specifies the authentication type. Possible options are: `password`, `no-password-required` or `iam`.
        :param Sequence[str] passwords: Specifies the passwords to use for authentication if `type` is set to `password`.
        """
        pulumi.set(__self__, "type", type)
        if password_count is not None:
            pulumi.set(__self__, "password_count", password_count)
        if passwords is not None:
            pulumi.set(__self__, "passwords", passwords)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the authentication type. Possible options are: `password`, `no-password-required` or `iam`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="passwordCount")
    def password_count(self) -> Optional[int]:
        return pulumi.get(self, "password_count")

    @property
    @pulumi.getter
    def passwords(self) -> Optional[Sequence[str]]:
        """
        Specifies the passwords to use for authentication if `type` is set to `password`.
        """
        return pulumi.get(self, "passwords")


@pulumi.output_type
class GetClusterCacheNodeResult(dict):
    def __init__(__self__, *,
                 address: str,
                 availability_zone: str,
                 id: str,
                 outpost_arn: str,
                 port: int):
        """
        :param str availability_zone: Availability Zone for the cache cluster.
        :param int port: The port number on which each of the cache nodes will
               accept connections.
        """
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "availability_zone", availability_zone)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "outpost_arn", outpost_arn)
        pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def address(self) -> str:
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> str:
        """
        Availability Zone for the cache cluster.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> str:
        return pulumi.get(self, "outpost_arn")

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port number on which each of the cache nodes will
        accept connections.
        """
        return pulumi.get(self, "port")


@pulumi.output_type
class GetClusterLogDeliveryConfigurationResult(dict):
    def __init__(__self__, *,
                 destination: str,
                 destination_type: str,
                 log_format: str,
                 log_type: str):
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter
    def destination(self) -> str:
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> str:
        return pulumi.get(self, "destination_type")

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> str:
        return pulumi.get(self, "log_format")

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        return pulumi.get(self, "log_type")


@pulumi.output_type
class GetReplicationGroupLogDeliveryConfigurationResult(dict):
    def __init__(__self__, *,
                 destination: str,
                 destination_type: str,
                 log_format: str,
                 log_type: str):
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter
    def destination(self) -> str:
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> str:
        return pulumi.get(self, "destination_type")

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> str:
        return pulumi.get(self, "log_format")

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        return pulumi.get(self, "log_type")


@pulumi.output_type
class GetUserAuthenticationModeResult(dict):
    def __init__(__self__, *,
                 password_count: Optional[int] = None,
                 type: Optional[str] = None):
        if password_count is not None:
            pulumi.set(__self__, "password_count", password_count)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="passwordCount")
    def password_count(self) -> Optional[int]:
        return pulumi.get(self, "password_count")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        return pulumi.get(self, "type")


