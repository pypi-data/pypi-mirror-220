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

__all__ = ['FsxOpenZfsFileSystemArgs', 'FsxOpenZfsFileSystem']

@pulumi.input_type
class FsxOpenZfsFileSystemArgs:
    def __init__(__self__, *,
                 fsx_filesystem_arn: pulumi.Input[str],
                 protocol: pulumi.Input['FsxOpenZfsFileSystemProtocolArgs'],
                 security_group_arns: pulumi.Input[Sequence[pulumi.Input[str]]],
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a FsxOpenZfsFileSystem resource.
        :param pulumi.Input[str] fsx_filesystem_arn: The Amazon Resource Name (ARN) for the FSx for OpenZfs file system.
        :param pulumi.Input['FsxOpenZfsFileSystemProtocolArgs'] protocol: The type of protocol that DataSync uses to access your file system. See below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_arns: The Amazon Resource Names (ARNs) of the security groups that are to use to configure the FSx for openzfs file system.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Must start with `/fsx`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "fsx_filesystem_arn", fsx_filesystem_arn)
        pulumi.set(__self__, "protocol", protocol)
        pulumi.set(__self__, "security_group_arns", security_group_arns)
        if subdirectory is not None:
            pulumi.set(__self__, "subdirectory", subdirectory)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="fsxFilesystemArn")
    def fsx_filesystem_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) for the FSx for OpenZfs file system.
        """
        return pulumi.get(self, "fsx_filesystem_arn")

    @fsx_filesystem_arn.setter
    def fsx_filesystem_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "fsx_filesystem_arn", value)

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Input['FsxOpenZfsFileSystemProtocolArgs']:
        """
        The type of protocol that DataSync uses to access your file system. See below.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: pulumi.Input['FsxOpenZfsFileSystemProtocolArgs']):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="securityGroupArns")
    def security_group_arns(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The Amazon Resource Names (ARNs) of the security groups that are to use to configure the FSx for openzfs file system.
        """
        return pulumi.get(self, "security_group_arns")

    @security_group_arns.setter
    def security_group_arns(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "security_group_arns", value)

    @property
    @pulumi.getter
    def subdirectory(self) -> Optional[pulumi.Input[str]]:
        """
        Subdirectory to perform actions as source or destination. Must start with `/fsx`.
        """
        return pulumi.get(self, "subdirectory")

    @subdirectory.setter
    def subdirectory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subdirectory", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value pairs of resource tags to assign to the DataSync Location. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _FsxOpenZfsFileSystemState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 creation_time: Optional[pulumi.Input[str]] = None,
                 fsx_filesystem_arn: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input['FsxOpenZfsFileSystemProtocolArgs']] = None,
                 security_group_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 uri: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering FsxOpenZfsFileSystem resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the DataSync Location.
        :param pulumi.Input[str] creation_time: The time that the FSx for openzfs location was created.
        :param pulumi.Input[str] fsx_filesystem_arn: The Amazon Resource Name (ARN) for the FSx for OpenZfs file system.
        :param pulumi.Input['FsxOpenZfsFileSystemProtocolArgs'] protocol: The type of protocol that DataSync uses to access your file system. See below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_arns: The Amazon Resource Names (ARNs) of the security groups that are to use to configure the FSx for openzfs file system.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Must start with `/fsx`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] uri: The URL of the FSx for openzfs location that was described.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if creation_time is not None:
            pulumi.set(__self__, "creation_time", creation_time)
        if fsx_filesystem_arn is not None:
            pulumi.set(__self__, "fsx_filesystem_arn", fsx_filesystem_arn)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if security_group_arns is not None:
            pulumi.set(__self__, "security_group_arns", security_group_arns)
        if subdirectory is not None:
            pulumi.set(__self__, "subdirectory", subdirectory)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if uri is not None:
            pulumi.set(__self__, "uri", uri)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the DataSync Location.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time that the FSx for openzfs location was created.
        """
        return pulumi.get(self, "creation_time")

    @creation_time.setter
    def creation_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creation_time", value)

    @property
    @pulumi.getter(name="fsxFilesystemArn")
    def fsx_filesystem_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) for the FSx for OpenZfs file system.
        """
        return pulumi.get(self, "fsx_filesystem_arn")

    @fsx_filesystem_arn.setter
    def fsx_filesystem_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fsx_filesystem_arn", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input['FsxOpenZfsFileSystemProtocolArgs']]:
        """
        The type of protocol that DataSync uses to access your file system. See below.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input['FsxOpenZfsFileSystemProtocolArgs']]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="securityGroupArns")
    def security_group_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The Amazon Resource Names (ARNs) of the security groups that are to use to configure the FSx for openzfs file system.
        """
        return pulumi.get(self, "security_group_arns")

    @security_group_arns.setter
    def security_group_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_group_arns", value)

    @property
    @pulumi.getter
    def subdirectory(self) -> Optional[pulumi.Input[str]]:
        """
        Subdirectory to perform actions as source or destination. Must start with `/fsx`.
        """
        return pulumi.get(self, "subdirectory")

    @subdirectory.setter
    def subdirectory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subdirectory", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value pairs of resource tags to assign to the DataSync Location. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter
    def uri(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the FSx for openzfs location that was described.
        """
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uri", value)


class FsxOpenZfsFileSystem(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 fsx_filesystem_arn: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[pulumi.InputType['FsxOpenZfsFileSystemProtocolArgs']]] = None,
                 security_group_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an AWS DataSync FSx OpenZfs Location.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.datasync.FsxOpenZfsFileSystem("example",
            fsx_filesystem_arn=aws_fsx_openzfs_file_system["example"]["arn"],
            security_group_arns=[aws_security_group["example"]["arn"]],
            protocol=aws.datasync.FsxOpenZfsFileSystemProtocolArgs(
                nfs=aws.datasync.FsxOpenZfsFileSystemProtocolNfsArgs(
                    mount_options=aws.datasync.FsxOpenZfsFileSystemProtocolNfsMountOptionsArgs(
                        version="AUTOMATIC",
                    ),
                ),
            ))
        ```

        ## Import

        `aws_datasync_location_fsx_openzfs_file_system` can be imported by using the `DataSync-ARN#FSx-openzfs-ARN`, e.g.,

        ```sh
         $ pulumi import aws:datasync/fsxOpenZfsFileSystem:FsxOpenZfsFileSystem example arn:aws:datasync:us-west-2:123456789012:location/loc-12345678901234567#arn:aws:fsx:us-west-2:123456789012:file-system/fs-08e04cd442c1bb94a
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] fsx_filesystem_arn: The Amazon Resource Name (ARN) for the FSx for OpenZfs file system.
        :param pulumi.Input[pulumi.InputType['FsxOpenZfsFileSystemProtocolArgs']] protocol: The type of protocol that DataSync uses to access your file system. See below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_arns: The Amazon Resource Names (ARNs) of the security groups that are to use to configure the FSx for openzfs file system.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Must start with `/fsx`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FsxOpenZfsFileSystemArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an AWS DataSync FSx OpenZfs Location.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.datasync.FsxOpenZfsFileSystem("example",
            fsx_filesystem_arn=aws_fsx_openzfs_file_system["example"]["arn"],
            security_group_arns=[aws_security_group["example"]["arn"]],
            protocol=aws.datasync.FsxOpenZfsFileSystemProtocolArgs(
                nfs=aws.datasync.FsxOpenZfsFileSystemProtocolNfsArgs(
                    mount_options=aws.datasync.FsxOpenZfsFileSystemProtocolNfsMountOptionsArgs(
                        version="AUTOMATIC",
                    ),
                ),
            ))
        ```

        ## Import

        `aws_datasync_location_fsx_openzfs_file_system` can be imported by using the `DataSync-ARN#FSx-openzfs-ARN`, e.g.,

        ```sh
         $ pulumi import aws:datasync/fsxOpenZfsFileSystem:FsxOpenZfsFileSystem example arn:aws:datasync:us-west-2:123456789012:location/loc-12345678901234567#arn:aws:fsx:us-west-2:123456789012:file-system/fs-08e04cd442c1bb94a
        ```

        :param str resource_name: The name of the resource.
        :param FsxOpenZfsFileSystemArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FsxOpenZfsFileSystemArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 fsx_filesystem_arn: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[pulumi.InputType['FsxOpenZfsFileSystemProtocolArgs']]] = None,
                 security_group_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FsxOpenZfsFileSystemArgs.__new__(FsxOpenZfsFileSystemArgs)

            if fsx_filesystem_arn is None and not opts.urn:
                raise TypeError("Missing required property 'fsx_filesystem_arn'")
            __props__.__dict__["fsx_filesystem_arn"] = fsx_filesystem_arn
            if protocol is None and not opts.urn:
                raise TypeError("Missing required property 'protocol'")
            __props__.__dict__["protocol"] = protocol
            if security_group_arns is None and not opts.urn:
                raise TypeError("Missing required property 'security_group_arns'")
            __props__.__dict__["security_group_arns"] = security_group_arns
            __props__.__dict__["subdirectory"] = subdirectory
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["tags_all"] = None
            __props__.__dict__["uri"] = None
        super(FsxOpenZfsFileSystem, __self__).__init__(
            'aws:datasync/fsxOpenZfsFileSystem:FsxOpenZfsFileSystem',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            creation_time: Optional[pulumi.Input[str]] = None,
            fsx_filesystem_arn: Optional[pulumi.Input[str]] = None,
            protocol: Optional[pulumi.Input[pulumi.InputType['FsxOpenZfsFileSystemProtocolArgs']]] = None,
            security_group_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            subdirectory: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            uri: Optional[pulumi.Input[str]] = None) -> 'FsxOpenZfsFileSystem':
        """
        Get an existing FsxOpenZfsFileSystem resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the DataSync Location.
        :param pulumi.Input[str] creation_time: The time that the FSx for openzfs location was created.
        :param pulumi.Input[str] fsx_filesystem_arn: The Amazon Resource Name (ARN) for the FSx for OpenZfs file system.
        :param pulumi.Input[pulumi.InputType['FsxOpenZfsFileSystemProtocolArgs']] protocol: The type of protocol that DataSync uses to access your file system. See below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_arns: The Amazon Resource Names (ARNs) of the security groups that are to use to configure the FSx for openzfs file system.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Must start with `/fsx`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] uri: The URL of the FSx for openzfs location that was described.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FsxOpenZfsFileSystemState.__new__(_FsxOpenZfsFileSystemState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["creation_time"] = creation_time
        __props__.__dict__["fsx_filesystem_arn"] = fsx_filesystem_arn
        __props__.__dict__["protocol"] = protocol
        __props__.__dict__["security_group_arns"] = security_group_arns
        __props__.__dict__["subdirectory"] = subdirectory
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["uri"] = uri
        return FsxOpenZfsFileSystem(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the DataSync Location.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        The time that the FSx for openzfs location was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="fsxFilesystemArn")
    def fsx_filesystem_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) for the FSx for OpenZfs file system.
        """
        return pulumi.get(self, "fsx_filesystem_arn")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output['outputs.FsxOpenZfsFileSystemProtocol']:
        """
        The type of protocol that DataSync uses to access your file system. See below.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="securityGroupArns")
    def security_group_arns(self) -> pulumi.Output[Sequence[str]]:
        """
        The Amazon Resource Names (ARNs) of the security groups that are to use to configure the FSx for openzfs file system.
        """
        return pulumi.get(self, "security_group_arns")

    @property
    @pulumi.getter
    def subdirectory(self) -> pulumi.Output[str]:
        """
        Subdirectory to perform actions as source or destination. Must start with `/fsx`.
        """
        return pulumi.get(self, "subdirectory")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value pairs of resource tags to assign to the DataSync Location. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Output[str]:
        """
        The URL of the FSx for openzfs location that was described.
        """
        return pulumi.get(self, "uri")

