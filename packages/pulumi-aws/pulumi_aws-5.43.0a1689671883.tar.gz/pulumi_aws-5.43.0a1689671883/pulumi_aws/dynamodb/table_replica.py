# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TableReplicaInitArgs', 'TableReplica']

@pulumi.input_type
class TableReplicaInitArgs:
    def __init__(__self__, *,
                 global_table_arn: pulumi.Input[str],
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 point_in_time_recovery: Optional[pulumi.Input[bool]] = None,
                 table_class_override: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a TableReplica resource.
        :param pulumi.Input[str] global_table_arn: ARN of the _main_ or global table which this resource will replicate.
               
               Optional arguments:
        :param pulumi.Input[str] kms_key_arn: ARN of the CMK that should be used for the AWS KMS encryption. This argument should only be used if the key is different from the default KMS-managed DynamoDB key, `alias/aws/dynamodb`. **Note:** This attribute will _not_ be populated with the ARN of _default_ keys.
        :param pulumi.Input[bool] point_in_time_recovery: Whether to enable Point In Time Recovery for the replica. Default is `false`.
        :param pulumi.Input[str] table_class_override: Storage class of the table replica. Valid values are `STANDARD` and `STANDARD_INFREQUENT_ACCESS`. If not used, the table replica will use the same class as the global table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to populate on the created table. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "global_table_arn", global_table_arn)
        if kms_key_arn is not None:
            pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if point_in_time_recovery is not None:
            pulumi.set(__self__, "point_in_time_recovery", point_in_time_recovery)
        if table_class_override is not None:
            pulumi.set(__self__, "table_class_override", table_class_override)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="globalTableArn")
    def global_table_arn(self) -> pulumi.Input[str]:
        """
        ARN of the _main_ or global table which this resource will replicate.

        Optional arguments:
        """
        return pulumi.get(self, "global_table_arn")

    @global_table_arn.setter
    def global_table_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "global_table_arn", value)

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the CMK that should be used for the AWS KMS encryption. This argument should only be used if the key is different from the default KMS-managed DynamoDB key, `alias/aws/dynamodb`. **Note:** This attribute will _not_ be populated with the ARN of _default_ keys.
        """
        return pulumi.get(self, "kms_key_arn")

    @kms_key_arn.setter
    def kms_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_arn", value)

    @property
    @pulumi.getter(name="pointInTimeRecovery")
    def point_in_time_recovery(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable Point In Time Recovery for the replica. Default is `false`.
        """
        return pulumi.get(self, "point_in_time_recovery")

    @point_in_time_recovery.setter
    def point_in_time_recovery(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "point_in_time_recovery", value)

    @property
    @pulumi.getter(name="tableClassOverride")
    def table_class_override(self) -> Optional[pulumi.Input[str]]:
        """
        Storage class of the table replica. Valid values are `STANDARD` and `STANDARD_INFREQUENT_ACCESS`. If not used, the table replica will use the same class as the global table.
        """
        return pulumi.get(self, "table_class_override")

    @table_class_override.setter
    def table_class_override(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table_class_override", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags to populate on the created table. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _TableReplicaState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 global_table_arn: Optional[pulumi.Input[str]] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 point_in_time_recovery: Optional[pulumi.Input[bool]] = None,
                 table_class_override: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering TableReplica resources.
        :param pulumi.Input[str] arn: ARN of the table replica.
        :param pulumi.Input[str] global_table_arn: ARN of the _main_ or global table which this resource will replicate.
               
               Optional arguments:
        :param pulumi.Input[str] kms_key_arn: ARN of the CMK that should be used for the AWS KMS encryption. This argument should only be used if the key is different from the default KMS-managed DynamoDB key, `alias/aws/dynamodb`. **Note:** This attribute will _not_ be populated with the ARN of _default_ keys.
        :param pulumi.Input[bool] point_in_time_recovery: Whether to enable Point In Time Recovery for the replica. Default is `false`.
        :param pulumi.Input[str] table_class_override: Storage class of the table replica. Valid values are `STANDARD` and `STANDARD_INFREQUENT_ACCESS`. If not used, the table replica will use the same class as the global table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to populate on the created table. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if global_table_arn is not None:
            pulumi.set(__self__, "global_table_arn", global_table_arn)
        if kms_key_arn is not None:
            pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if point_in_time_recovery is not None:
            pulumi.set(__self__, "point_in_time_recovery", point_in_time_recovery)
        if table_class_override is not None:
            pulumi.set(__self__, "table_class_override", table_class_override)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the table replica.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="globalTableArn")
    def global_table_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the _main_ or global table which this resource will replicate.

        Optional arguments:
        """
        return pulumi.get(self, "global_table_arn")

    @global_table_arn.setter
    def global_table_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "global_table_arn", value)

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the CMK that should be used for the AWS KMS encryption. This argument should only be used if the key is different from the default KMS-managed DynamoDB key, `alias/aws/dynamodb`. **Note:** This attribute will _not_ be populated with the ARN of _default_ keys.
        """
        return pulumi.get(self, "kms_key_arn")

    @kms_key_arn.setter
    def kms_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_arn", value)

    @property
    @pulumi.getter(name="pointInTimeRecovery")
    def point_in_time_recovery(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable Point In Time Recovery for the replica. Default is `false`.
        """
        return pulumi.get(self, "point_in_time_recovery")

    @point_in_time_recovery.setter
    def point_in_time_recovery(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "point_in_time_recovery", value)

    @property
    @pulumi.getter(name="tableClassOverride")
    def table_class_override(self) -> Optional[pulumi.Input[str]]:
        """
        Storage class of the table replica. Valid values are `STANDARD` and `STANDARD_INFREQUENT_ACCESS`. If not used, the table replica will use the same class as the global table.
        """
        return pulumi.get(self, "table_class_override")

    @table_class_override.setter
    def table_class_override(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table_class_override", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags to populate on the created table. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class TableReplica(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 global_table_arn: Optional[pulumi.Input[str]] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 point_in_time_recovery: Optional[pulumi.Input[bool]] = None,
                 table_class_override: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a DynamoDB table replica resource for [DynamoDB Global Tables V2 (version 2019.11.21)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/globaltables.V2.html).

        > **Note:** Use `lifecycle` `ignore_changes` for `replica` in the associated dynamodb.Table configuration.

        > **Note:** Do not use the `replica` configuration block of dynamodb.Table together with this resource as the two configuration options are mutually exclusive.

        ## Example Usage
        ### Basic Example

        ```python
        import pulumi
        import pulumi_aws as aws

        main = aws.Provider("main", region="us-west-2")
        alt = aws.Provider("alt", region="us-east-2")
        example_table = aws.dynamodb.Table("exampleTable",
            hash_key="BrodoBaggins",
            billing_mode="PAY_PER_REQUEST",
            stream_enabled=True,
            stream_view_type="NEW_AND_OLD_IMAGES",
            attributes=[aws.dynamodb.TableAttributeArgs(
                name="BrodoBaggins",
                type="S",
            )],
            opts=pulumi.ResourceOptions(provider="aws.main"))
        example_table_replica = aws.dynamodb.TableReplica("exampleTableReplica",
            global_table_arn=example_table.arn,
            tags={
                "Name": "IZPAWS",
                "Pozo": "Amargo",
            },
            opts=pulumi.ResourceOptions(provider="aws.alt"))
        ```

        ## Import

        DynamoDB table replicas can be imported using the `table-name:main-region`, _e.g._,

        ```sh
         $ pulumi import aws:dynamodb/tableReplica:TableReplica example TestTable:us-west-2
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] global_table_arn: ARN of the _main_ or global table which this resource will replicate.
               
               Optional arguments:
        :param pulumi.Input[str] kms_key_arn: ARN of the CMK that should be used for the AWS KMS encryption. This argument should only be used if the key is different from the default KMS-managed DynamoDB key, `alias/aws/dynamodb`. **Note:** This attribute will _not_ be populated with the ARN of _default_ keys.
        :param pulumi.Input[bool] point_in_time_recovery: Whether to enable Point In Time Recovery for the replica. Default is `false`.
        :param pulumi.Input[str] table_class_override: Storage class of the table replica. Valid values are `STANDARD` and `STANDARD_INFREQUENT_ACCESS`. If not used, the table replica will use the same class as the global table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to populate on the created table. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TableReplicaInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a DynamoDB table replica resource for [DynamoDB Global Tables V2 (version 2019.11.21)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/globaltables.V2.html).

        > **Note:** Use `lifecycle` `ignore_changes` for `replica` in the associated dynamodb.Table configuration.

        > **Note:** Do not use the `replica` configuration block of dynamodb.Table together with this resource as the two configuration options are mutually exclusive.

        ## Example Usage
        ### Basic Example

        ```python
        import pulumi
        import pulumi_aws as aws

        main = aws.Provider("main", region="us-west-2")
        alt = aws.Provider("alt", region="us-east-2")
        example_table = aws.dynamodb.Table("exampleTable",
            hash_key="BrodoBaggins",
            billing_mode="PAY_PER_REQUEST",
            stream_enabled=True,
            stream_view_type="NEW_AND_OLD_IMAGES",
            attributes=[aws.dynamodb.TableAttributeArgs(
                name="BrodoBaggins",
                type="S",
            )],
            opts=pulumi.ResourceOptions(provider="aws.main"))
        example_table_replica = aws.dynamodb.TableReplica("exampleTableReplica",
            global_table_arn=example_table.arn,
            tags={
                "Name": "IZPAWS",
                "Pozo": "Amargo",
            },
            opts=pulumi.ResourceOptions(provider="aws.alt"))
        ```

        ## Import

        DynamoDB table replicas can be imported using the `table-name:main-region`, _e.g._,

        ```sh
         $ pulumi import aws:dynamodb/tableReplica:TableReplica example TestTable:us-west-2
        ```

        :param str resource_name: The name of the resource.
        :param TableReplicaInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TableReplicaInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 global_table_arn: Optional[pulumi.Input[str]] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 point_in_time_recovery: Optional[pulumi.Input[bool]] = None,
                 table_class_override: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TableReplicaInitArgs.__new__(TableReplicaInitArgs)

            if global_table_arn is None and not opts.urn:
                raise TypeError("Missing required property 'global_table_arn'")
            __props__.__dict__["global_table_arn"] = global_table_arn
            __props__.__dict__["kms_key_arn"] = kms_key_arn
            __props__.__dict__["point_in_time_recovery"] = point_in_time_recovery
            __props__.__dict__["table_class_override"] = table_class_override
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(TableReplica, __self__).__init__(
            'aws:dynamodb/tableReplica:TableReplica',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            global_table_arn: Optional[pulumi.Input[str]] = None,
            kms_key_arn: Optional[pulumi.Input[str]] = None,
            point_in_time_recovery: Optional[pulumi.Input[bool]] = None,
            table_class_override: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'TableReplica':
        """
        Get an existing TableReplica resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the table replica.
        :param pulumi.Input[str] global_table_arn: ARN of the _main_ or global table which this resource will replicate.
               
               Optional arguments:
        :param pulumi.Input[str] kms_key_arn: ARN of the CMK that should be used for the AWS KMS encryption. This argument should only be used if the key is different from the default KMS-managed DynamoDB key, `alias/aws/dynamodb`. **Note:** This attribute will _not_ be populated with the ARN of _default_ keys.
        :param pulumi.Input[bool] point_in_time_recovery: Whether to enable Point In Time Recovery for the replica. Default is `false`.
        :param pulumi.Input[str] table_class_override: Storage class of the table replica. Valid values are `STANDARD` and `STANDARD_INFREQUENT_ACCESS`. If not used, the table replica will use the same class as the global table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to populate on the created table. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TableReplicaState.__new__(_TableReplicaState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["global_table_arn"] = global_table_arn
        __props__.__dict__["kms_key_arn"] = kms_key_arn
        __props__.__dict__["point_in_time_recovery"] = point_in_time_recovery
        __props__.__dict__["table_class_override"] = table_class_override
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return TableReplica(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the table replica.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="globalTableArn")
    def global_table_arn(self) -> pulumi.Output[str]:
        """
        ARN of the _main_ or global table which this resource will replicate.

        Optional arguments:
        """
        return pulumi.get(self, "global_table_arn")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> pulumi.Output[str]:
        """
        ARN of the CMK that should be used for the AWS KMS encryption. This argument should only be used if the key is different from the default KMS-managed DynamoDB key, `alias/aws/dynamodb`. **Note:** This attribute will _not_ be populated with the ARN of _default_ keys.
        """
        return pulumi.get(self, "kms_key_arn")

    @property
    @pulumi.getter(name="pointInTimeRecovery")
    def point_in_time_recovery(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to enable Point In Time Recovery for the replica. Default is `false`.
        """
        return pulumi.get(self, "point_in_time_recovery")

    @property
    @pulumi.getter(name="tableClassOverride")
    def table_class_override(self) -> pulumi.Output[Optional[str]]:
        """
        Storage class of the table replica. Valid values are `STANDARD` and `STANDARD_INFREQUENT_ACCESS`. If not used, the table replica will use the same class as the global table.
        """
        return pulumi.get(self, "table_class_override")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of tags to populate on the created table. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

