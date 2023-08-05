# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SnapshotArgs', 'Snapshot']

@pulumi.input_type
class SnapshotArgs:
    def __init__(__self__, *,
                 namespace_name: pulumi.Input[str],
                 snapshot_name: pulumi.Input[str],
                 retention_period: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Snapshot resource.
        :param pulumi.Input[str] namespace_name: The namespace to create a snapshot for.
        :param pulumi.Input[str] snapshot_name: The name of the snapshot.
        :param pulumi.Input[int] retention_period: How long to retain the created snapshot. Default value is `-1`.
        """
        pulumi.set(__self__, "namespace_name", namespace_name)
        pulumi.set(__self__, "snapshot_name", snapshot_name)
        if retention_period is not None:
            pulumi.set(__self__, "retention_period", retention_period)

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> pulumi.Input[str]:
        """
        The namespace to create a snapshot for.
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="snapshotName")
    def snapshot_name(self) -> pulumi.Input[str]:
        """
        The name of the snapshot.
        """
        return pulumi.get(self, "snapshot_name")

    @snapshot_name.setter
    def snapshot_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "snapshot_name", value)

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> Optional[pulumi.Input[int]]:
        """
        How long to retain the created snapshot. Default value is `-1`.
        """
        return pulumi.get(self, "retention_period")

    @retention_period.setter
    def retention_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retention_period", value)


@pulumi.input_type
class _SnapshotState:
    def __init__(__self__, *,
                 accounts_with_provisioned_restore_accesses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 accounts_with_restore_accesses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 admin_username: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 namespace_arn: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 owner_account: Optional[pulumi.Input[str]] = None,
                 retention_period: Optional[pulumi.Input[int]] = None,
                 snapshot_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Snapshot resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] accounts_with_provisioned_restore_accesses: All of the Amazon Web Services accounts that have access to restore a snapshot to a provisioned cluster.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] accounts_with_restore_accesses: All of the Amazon Web Services accounts that have access to restore a snapshot to a namespace.
        :param pulumi.Input[str] admin_username: The username of the database within a snapshot.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the snapshot.
        :param pulumi.Input[str] kms_key_id: The unique identifier of the KMS key used to encrypt the snapshot.
        :param pulumi.Input[str] namespace_arn: The Amazon Resource Name (ARN) of the namespace the snapshot was created from.
        :param pulumi.Input[str] namespace_name: The namespace to create a snapshot for.
        :param pulumi.Input[str] owner_account: The owner Amazon Web Services; account of the snapshot.
        :param pulumi.Input[int] retention_period: How long to retain the created snapshot. Default value is `-1`.
        :param pulumi.Input[str] snapshot_name: The name of the snapshot.
        """
        if accounts_with_provisioned_restore_accesses is not None:
            pulumi.set(__self__, "accounts_with_provisioned_restore_accesses", accounts_with_provisioned_restore_accesses)
        if accounts_with_restore_accesses is not None:
            pulumi.set(__self__, "accounts_with_restore_accesses", accounts_with_restore_accesses)
        if admin_username is not None:
            pulumi.set(__self__, "admin_username", admin_username)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if namespace_arn is not None:
            pulumi.set(__self__, "namespace_arn", namespace_arn)
        if namespace_name is not None:
            pulumi.set(__self__, "namespace_name", namespace_name)
        if owner_account is not None:
            pulumi.set(__self__, "owner_account", owner_account)
        if retention_period is not None:
            pulumi.set(__self__, "retention_period", retention_period)
        if snapshot_name is not None:
            pulumi.set(__self__, "snapshot_name", snapshot_name)

    @property
    @pulumi.getter(name="accountsWithProvisionedRestoreAccesses")
    def accounts_with_provisioned_restore_accesses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        All of the Amazon Web Services accounts that have access to restore a snapshot to a provisioned cluster.
        """
        return pulumi.get(self, "accounts_with_provisioned_restore_accesses")

    @accounts_with_provisioned_restore_accesses.setter
    def accounts_with_provisioned_restore_accesses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "accounts_with_provisioned_restore_accesses", value)

    @property
    @pulumi.getter(name="accountsWithRestoreAccesses")
    def accounts_with_restore_accesses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        All of the Amazon Web Services accounts that have access to restore a snapshot to a namespace.
        """
        return pulumi.get(self, "accounts_with_restore_accesses")

    @accounts_with_restore_accesses.setter
    def accounts_with_restore_accesses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "accounts_with_restore_accesses", value)

    @property
    @pulumi.getter(name="adminUsername")
    def admin_username(self) -> Optional[pulumi.Input[str]]:
        """
        The username of the database within a snapshot.
        """
        return pulumi.get(self, "admin_username")

    @admin_username.setter
    def admin_username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "admin_username", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the snapshot.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier of the KMS key used to encrypt the snapshot.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter(name="namespaceArn")
    def namespace_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the namespace the snapshot was created from.
        """
        return pulumi.get(self, "namespace_arn")

    @namespace_arn.setter
    def namespace_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace_arn", value)

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to create a snapshot for.
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="ownerAccount")
    def owner_account(self) -> Optional[pulumi.Input[str]]:
        """
        The owner Amazon Web Services; account of the snapshot.
        """
        return pulumi.get(self, "owner_account")

    @owner_account.setter
    def owner_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_account", value)

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> Optional[pulumi.Input[int]]:
        """
        How long to retain the created snapshot. Default value is `-1`.
        """
        return pulumi.get(self, "retention_period")

    @retention_period.setter
    def retention_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retention_period", value)

    @property
    @pulumi.getter(name="snapshotName")
    def snapshot_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the snapshot.
        """
        return pulumi.get(self, "snapshot_name")

    @snapshot_name.setter
    def snapshot_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "snapshot_name", value)


class Snapshot(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 retention_period: Optional[pulumi.Input[int]] = None,
                 snapshot_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a new Amazon Redshift Serverless Snapshot.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.redshiftserverless.Snapshot("example",
            namespace_name=aws_redshiftserverless_workgroup["example"]["namespace_name"],
            snapshot_name="example")
        ```

        ## Import

        Redshift Serverless Snapshots can be imported using the `snapshot_name`, e.g.,

        ```sh
         $ pulumi import aws:redshiftserverless/snapshot:Snapshot example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] namespace_name: The namespace to create a snapshot for.
        :param pulumi.Input[int] retention_period: How long to retain the created snapshot. Default value is `-1`.
        :param pulumi.Input[str] snapshot_name: The name of the snapshot.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SnapshotArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a new Amazon Redshift Serverless Snapshot.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.redshiftserverless.Snapshot("example",
            namespace_name=aws_redshiftserverless_workgroup["example"]["namespace_name"],
            snapshot_name="example")
        ```

        ## Import

        Redshift Serverless Snapshots can be imported using the `snapshot_name`, e.g.,

        ```sh
         $ pulumi import aws:redshiftserverless/snapshot:Snapshot example example
        ```

        :param str resource_name: The name of the resource.
        :param SnapshotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SnapshotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 retention_period: Optional[pulumi.Input[int]] = None,
                 snapshot_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SnapshotArgs.__new__(SnapshotArgs)

            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__["namespace_name"] = namespace_name
            __props__.__dict__["retention_period"] = retention_period
            if snapshot_name is None and not opts.urn:
                raise TypeError("Missing required property 'snapshot_name'")
            __props__.__dict__["snapshot_name"] = snapshot_name
            __props__.__dict__["accounts_with_provisioned_restore_accesses"] = None
            __props__.__dict__["accounts_with_restore_accesses"] = None
            __props__.__dict__["admin_username"] = None
            __props__.__dict__["arn"] = None
            __props__.__dict__["kms_key_id"] = None
            __props__.__dict__["namespace_arn"] = None
            __props__.__dict__["owner_account"] = None
        super(Snapshot, __self__).__init__(
            'aws:redshiftserverless/snapshot:Snapshot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accounts_with_provisioned_restore_accesses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            accounts_with_restore_accesses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            admin_username: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            kms_key_id: Optional[pulumi.Input[str]] = None,
            namespace_arn: Optional[pulumi.Input[str]] = None,
            namespace_name: Optional[pulumi.Input[str]] = None,
            owner_account: Optional[pulumi.Input[str]] = None,
            retention_period: Optional[pulumi.Input[int]] = None,
            snapshot_name: Optional[pulumi.Input[str]] = None) -> 'Snapshot':
        """
        Get an existing Snapshot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] accounts_with_provisioned_restore_accesses: All of the Amazon Web Services accounts that have access to restore a snapshot to a provisioned cluster.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] accounts_with_restore_accesses: All of the Amazon Web Services accounts that have access to restore a snapshot to a namespace.
        :param pulumi.Input[str] admin_username: The username of the database within a snapshot.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the snapshot.
        :param pulumi.Input[str] kms_key_id: The unique identifier of the KMS key used to encrypt the snapshot.
        :param pulumi.Input[str] namespace_arn: The Amazon Resource Name (ARN) of the namespace the snapshot was created from.
        :param pulumi.Input[str] namespace_name: The namespace to create a snapshot for.
        :param pulumi.Input[str] owner_account: The owner Amazon Web Services; account of the snapshot.
        :param pulumi.Input[int] retention_period: How long to retain the created snapshot. Default value is `-1`.
        :param pulumi.Input[str] snapshot_name: The name of the snapshot.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SnapshotState.__new__(_SnapshotState)

        __props__.__dict__["accounts_with_provisioned_restore_accesses"] = accounts_with_provisioned_restore_accesses
        __props__.__dict__["accounts_with_restore_accesses"] = accounts_with_restore_accesses
        __props__.__dict__["admin_username"] = admin_username
        __props__.__dict__["arn"] = arn
        __props__.__dict__["kms_key_id"] = kms_key_id
        __props__.__dict__["namespace_arn"] = namespace_arn
        __props__.__dict__["namespace_name"] = namespace_name
        __props__.__dict__["owner_account"] = owner_account
        __props__.__dict__["retention_period"] = retention_period
        __props__.__dict__["snapshot_name"] = snapshot_name
        return Snapshot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountsWithProvisionedRestoreAccesses")
    def accounts_with_provisioned_restore_accesses(self) -> pulumi.Output[Sequence[str]]:
        """
        All of the Amazon Web Services accounts that have access to restore a snapshot to a provisioned cluster.
        """
        return pulumi.get(self, "accounts_with_provisioned_restore_accesses")

    @property
    @pulumi.getter(name="accountsWithRestoreAccesses")
    def accounts_with_restore_accesses(self) -> pulumi.Output[Sequence[str]]:
        """
        All of the Amazon Web Services accounts that have access to restore a snapshot to a namespace.
        """
        return pulumi.get(self, "accounts_with_restore_accesses")

    @property
    @pulumi.getter(name="adminUsername")
    def admin_username(self) -> pulumi.Output[str]:
        """
        The username of the database within a snapshot.
        """
        return pulumi.get(self, "admin_username")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the snapshot.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[str]:
        """
        The unique identifier of the KMS key used to encrypt the snapshot.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="namespaceArn")
    def namespace_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the namespace the snapshot was created from.
        """
        return pulumi.get(self, "namespace_arn")

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> pulumi.Output[str]:
        """
        The namespace to create a snapshot for.
        """
        return pulumi.get(self, "namespace_name")

    @property
    @pulumi.getter(name="ownerAccount")
    def owner_account(self) -> pulumi.Output[str]:
        """
        The owner Amazon Web Services; account of the snapshot.
        """
        return pulumi.get(self, "owner_account")

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> pulumi.Output[Optional[int]]:
        """
        How long to retain the created snapshot. Default value is `-1`.
        """
        return pulumi.get(self, "retention_period")

    @property
    @pulumi.getter(name="snapshotName")
    def snapshot_name(self) -> pulumi.Output[str]:
        """
        The name of the snapshot.
        """
        return pulumi.get(self, "snapshot_name")

