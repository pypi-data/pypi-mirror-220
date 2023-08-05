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

__all__ = ['TableArgs', 'Table']

@pulumi.input_type
class TableArgs:
    def __init__(__self__, *,
                 keyspace_name: pulumi.Input[str],
                 schema_definition: pulumi.Input['TableSchemaDefinitionArgs'],
                 table_name: pulumi.Input[str],
                 capacity_specification: Optional[pulumi.Input['TableCapacitySpecificationArgs']] = None,
                 comment: Optional[pulumi.Input['TableCommentArgs']] = None,
                 default_time_to_live: Optional[pulumi.Input[int]] = None,
                 encryption_specification: Optional[pulumi.Input['TableEncryptionSpecificationArgs']] = None,
                 point_in_time_recovery: Optional[pulumi.Input['TablePointInTimeRecoveryArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ttl: Optional[pulumi.Input['TableTtlArgs']] = None):
        """
        The set of arguments for constructing a Table resource.
        :param pulumi.Input[str] keyspace_name: The name of the keyspace that the table is going to be created in.
        :param pulumi.Input['TableSchemaDefinitionArgs'] schema_definition: Describes the schema of the table.
        :param pulumi.Input[str] table_name: The name of the table.
               
               The following arguments are optional:
        :param pulumi.Input['TableCapacitySpecificationArgs'] capacity_specification: Specifies the read/write throughput capacity mode for the table.
        :param pulumi.Input['TableCommentArgs'] comment: A description of the table.
        :param pulumi.Input[int] default_time_to_live: The default Time to Live setting in seconds for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl).
        :param pulumi.Input['TableEncryptionSpecificationArgs'] encryption_specification: Specifies how the encryption key for encryption at rest is managed for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html).
        :param pulumi.Input['TablePointInTimeRecoveryArgs'] point_in_time_recovery: Specifies if point-in-time recovery is enabled or disabled for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/PointInTimeRecovery.html).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input['TableTtlArgs'] ttl: Enables Time to Live custom settings for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL.html).
        """
        pulumi.set(__self__, "keyspace_name", keyspace_name)
        pulumi.set(__self__, "schema_definition", schema_definition)
        pulumi.set(__self__, "table_name", table_name)
        if capacity_specification is not None:
            pulumi.set(__self__, "capacity_specification", capacity_specification)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if default_time_to_live is not None:
            pulumi.set(__self__, "default_time_to_live", default_time_to_live)
        if encryption_specification is not None:
            pulumi.set(__self__, "encryption_specification", encryption_specification)
        if point_in_time_recovery is not None:
            pulumi.set(__self__, "point_in_time_recovery", point_in_time_recovery)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter(name="keyspaceName")
    def keyspace_name(self) -> pulumi.Input[str]:
        """
        The name of the keyspace that the table is going to be created in.
        """
        return pulumi.get(self, "keyspace_name")

    @keyspace_name.setter
    def keyspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "keyspace_name", value)

    @property
    @pulumi.getter(name="schemaDefinition")
    def schema_definition(self) -> pulumi.Input['TableSchemaDefinitionArgs']:
        """
        Describes the schema of the table.
        """
        return pulumi.get(self, "schema_definition")

    @schema_definition.setter
    def schema_definition(self, value: pulumi.Input['TableSchemaDefinitionArgs']):
        pulumi.set(self, "schema_definition", value)

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> pulumi.Input[str]:
        """
        The name of the table.

        The following arguments are optional:
        """
        return pulumi.get(self, "table_name")

    @table_name.setter
    def table_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "table_name", value)

    @property
    @pulumi.getter(name="capacitySpecification")
    def capacity_specification(self) -> Optional[pulumi.Input['TableCapacitySpecificationArgs']]:
        """
        Specifies the read/write throughput capacity mode for the table.
        """
        return pulumi.get(self, "capacity_specification")

    @capacity_specification.setter
    def capacity_specification(self, value: Optional[pulumi.Input['TableCapacitySpecificationArgs']]):
        pulumi.set(self, "capacity_specification", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input['TableCommentArgs']]:
        """
        A description of the table.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input['TableCommentArgs']]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="defaultTimeToLive")
    def default_time_to_live(self) -> Optional[pulumi.Input[int]]:
        """
        The default Time to Live setting in seconds for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl).
        """
        return pulumi.get(self, "default_time_to_live")

    @default_time_to_live.setter
    def default_time_to_live(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "default_time_to_live", value)

    @property
    @pulumi.getter(name="encryptionSpecification")
    def encryption_specification(self) -> Optional[pulumi.Input['TableEncryptionSpecificationArgs']]:
        """
        Specifies how the encryption key for encryption at rest is managed for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html).
        """
        return pulumi.get(self, "encryption_specification")

    @encryption_specification.setter
    def encryption_specification(self, value: Optional[pulumi.Input['TableEncryptionSpecificationArgs']]):
        pulumi.set(self, "encryption_specification", value)

    @property
    @pulumi.getter(name="pointInTimeRecovery")
    def point_in_time_recovery(self) -> Optional[pulumi.Input['TablePointInTimeRecoveryArgs']]:
        """
        Specifies if point-in-time recovery is enabled or disabled for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/PointInTimeRecovery.html).
        """
        return pulumi.get(self, "point_in_time_recovery")

    @point_in_time_recovery.setter
    def point_in_time_recovery(self, value: Optional[pulumi.Input['TablePointInTimeRecoveryArgs']]):
        pulumi.set(self, "point_in_time_recovery", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input['TableTtlArgs']]:
        """
        Enables Time to Live custom settings for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL.html).
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input['TableTtlArgs']]):
        pulumi.set(self, "ttl", value)


@pulumi.input_type
class _TableState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 capacity_specification: Optional[pulumi.Input['TableCapacitySpecificationArgs']] = None,
                 comment: Optional[pulumi.Input['TableCommentArgs']] = None,
                 default_time_to_live: Optional[pulumi.Input[int]] = None,
                 encryption_specification: Optional[pulumi.Input['TableEncryptionSpecificationArgs']] = None,
                 keyspace_name: Optional[pulumi.Input[str]] = None,
                 point_in_time_recovery: Optional[pulumi.Input['TablePointInTimeRecoveryArgs']] = None,
                 schema_definition: Optional[pulumi.Input['TableSchemaDefinitionArgs']] = None,
                 table_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ttl: Optional[pulumi.Input['TableTtlArgs']] = None):
        """
        Input properties used for looking up and filtering Table resources.
        :param pulumi.Input[str] arn: The ARN of the table.
        :param pulumi.Input['TableCapacitySpecificationArgs'] capacity_specification: Specifies the read/write throughput capacity mode for the table.
        :param pulumi.Input['TableCommentArgs'] comment: A description of the table.
        :param pulumi.Input[int] default_time_to_live: The default Time to Live setting in seconds for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl).
        :param pulumi.Input['TableEncryptionSpecificationArgs'] encryption_specification: Specifies how the encryption key for encryption at rest is managed for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html).
        :param pulumi.Input[str] keyspace_name: The name of the keyspace that the table is going to be created in.
        :param pulumi.Input['TablePointInTimeRecoveryArgs'] point_in_time_recovery: Specifies if point-in-time recovery is enabled or disabled for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/PointInTimeRecovery.html).
        :param pulumi.Input['TableSchemaDefinitionArgs'] schema_definition: Describes the schema of the table.
        :param pulumi.Input[str] table_name: The name of the table.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input['TableTtlArgs'] ttl: Enables Time to Live custom settings for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL.html).
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if capacity_specification is not None:
            pulumi.set(__self__, "capacity_specification", capacity_specification)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if default_time_to_live is not None:
            pulumi.set(__self__, "default_time_to_live", default_time_to_live)
        if encryption_specification is not None:
            pulumi.set(__self__, "encryption_specification", encryption_specification)
        if keyspace_name is not None:
            pulumi.set(__self__, "keyspace_name", keyspace_name)
        if point_in_time_recovery is not None:
            pulumi.set(__self__, "point_in_time_recovery", point_in_time_recovery)
        if schema_definition is not None:
            pulumi.set(__self__, "schema_definition", schema_definition)
        if table_name is not None:
            pulumi.set(__self__, "table_name", table_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the table.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="capacitySpecification")
    def capacity_specification(self) -> Optional[pulumi.Input['TableCapacitySpecificationArgs']]:
        """
        Specifies the read/write throughput capacity mode for the table.
        """
        return pulumi.get(self, "capacity_specification")

    @capacity_specification.setter
    def capacity_specification(self, value: Optional[pulumi.Input['TableCapacitySpecificationArgs']]):
        pulumi.set(self, "capacity_specification", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input['TableCommentArgs']]:
        """
        A description of the table.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input['TableCommentArgs']]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="defaultTimeToLive")
    def default_time_to_live(self) -> Optional[pulumi.Input[int]]:
        """
        The default Time to Live setting in seconds for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl).
        """
        return pulumi.get(self, "default_time_to_live")

    @default_time_to_live.setter
    def default_time_to_live(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "default_time_to_live", value)

    @property
    @pulumi.getter(name="encryptionSpecification")
    def encryption_specification(self) -> Optional[pulumi.Input['TableEncryptionSpecificationArgs']]:
        """
        Specifies how the encryption key for encryption at rest is managed for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html).
        """
        return pulumi.get(self, "encryption_specification")

    @encryption_specification.setter
    def encryption_specification(self, value: Optional[pulumi.Input['TableEncryptionSpecificationArgs']]):
        pulumi.set(self, "encryption_specification", value)

    @property
    @pulumi.getter(name="keyspaceName")
    def keyspace_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the keyspace that the table is going to be created in.
        """
        return pulumi.get(self, "keyspace_name")

    @keyspace_name.setter
    def keyspace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "keyspace_name", value)

    @property
    @pulumi.getter(name="pointInTimeRecovery")
    def point_in_time_recovery(self) -> Optional[pulumi.Input['TablePointInTimeRecoveryArgs']]:
        """
        Specifies if point-in-time recovery is enabled or disabled for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/PointInTimeRecovery.html).
        """
        return pulumi.get(self, "point_in_time_recovery")

    @point_in_time_recovery.setter
    def point_in_time_recovery(self, value: Optional[pulumi.Input['TablePointInTimeRecoveryArgs']]):
        pulumi.set(self, "point_in_time_recovery", value)

    @property
    @pulumi.getter(name="schemaDefinition")
    def schema_definition(self) -> Optional[pulumi.Input['TableSchemaDefinitionArgs']]:
        """
        Describes the schema of the table.
        """
        return pulumi.get(self, "schema_definition")

    @schema_definition.setter
    def schema_definition(self, value: Optional[pulumi.Input['TableSchemaDefinitionArgs']]):
        pulumi.set(self, "schema_definition", value)

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the table.

        The following arguments are optional:
        """
        return pulumi.get(self, "table_name")

    @table_name.setter
    def table_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    def ttl(self) -> Optional[pulumi.Input['TableTtlArgs']]:
        """
        Enables Time to Live custom settings for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL.html).
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input['TableTtlArgs']]):
        pulumi.set(self, "ttl", value)


class Table(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 capacity_specification: Optional[pulumi.Input[pulumi.InputType['TableCapacitySpecificationArgs']]] = None,
                 comment: Optional[pulumi.Input[pulumi.InputType['TableCommentArgs']]] = None,
                 default_time_to_live: Optional[pulumi.Input[int]] = None,
                 encryption_specification: Optional[pulumi.Input[pulumi.InputType['TableEncryptionSpecificationArgs']]] = None,
                 keyspace_name: Optional[pulumi.Input[str]] = None,
                 point_in_time_recovery: Optional[pulumi.Input[pulumi.InputType['TablePointInTimeRecoveryArgs']]] = None,
                 schema_definition: Optional[pulumi.Input[pulumi.InputType['TableSchemaDefinitionArgs']]] = None,
                 table_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ttl: Optional[pulumi.Input[pulumi.InputType['TableTtlArgs']]] = None,
                 __props__=None):
        """
        Provides a Keyspaces Table.

        More information about Keyspaces tables can be found in the [Keyspaces Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/working-with-tables.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.keyspaces.Table("example",
            keyspace_name=aws_keyspaces_keyspace["example"]["name"],
            table_name="my_table",
            schema_definition=aws.keyspaces.TableSchemaDefinitionArgs(
                columns=[aws.keyspaces.TableSchemaDefinitionColumnArgs(
                    name="Message",
                    type="ASCII",
                )],
                partition_keys=[aws.keyspaces.TableSchemaDefinitionPartitionKeyArgs(
                    name="Message",
                )],
            ))
        ```

        ## Import

        Use the `keyspace_name` and `table_name` separated by `/` to import a table. For example

        ```sh
         $ pulumi import aws:keyspaces/table:Table example my_keyspace/my_table
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['TableCapacitySpecificationArgs']] capacity_specification: Specifies the read/write throughput capacity mode for the table.
        :param pulumi.Input[pulumi.InputType['TableCommentArgs']] comment: A description of the table.
        :param pulumi.Input[int] default_time_to_live: The default Time to Live setting in seconds for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl).
        :param pulumi.Input[pulumi.InputType['TableEncryptionSpecificationArgs']] encryption_specification: Specifies how the encryption key for encryption at rest is managed for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html).
        :param pulumi.Input[str] keyspace_name: The name of the keyspace that the table is going to be created in.
        :param pulumi.Input[pulumi.InputType['TablePointInTimeRecoveryArgs']] point_in_time_recovery: Specifies if point-in-time recovery is enabled or disabled for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/PointInTimeRecovery.html).
        :param pulumi.Input[pulumi.InputType['TableSchemaDefinitionArgs']] schema_definition: Describes the schema of the table.
        :param pulumi.Input[str] table_name: The name of the table.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[pulumi.InputType['TableTtlArgs']] ttl: Enables Time to Live custom settings for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL.html).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TableArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Keyspaces Table.

        More information about Keyspaces tables can be found in the [Keyspaces Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/working-with-tables.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.keyspaces.Table("example",
            keyspace_name=aws_keyspaces_keyspace["example"]["name"],
            table_name="my_table",
            schema_definition=aws.keyspaces.TableSchemaDefinitionArgs(
                columns=[aws.keyspaces.TableSchemaDefinitionColumnArgs(
                    name="Message",
                    type="ASCII",
                )],
                partition_keys=[aws.keyspaces.TableSchemaDefinitionPartitionKeyArgs(
                    name="Message",
                )],
            ))
        ```

        ## Import

        Use the `keyspace_name` and `table_name` separated by `/` to import a table. For example

        ```sh
         $ pulumi import aws:keyspaces/table:Table example my_keyspace/my_table
        ```

        :param str resource_name: The name of the resource.
        :param TableArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TableArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 capacity_specification: Optional[pulumi.Input[pulumi.InputType['TableCapacitySpecificationArgs']]] = None,
                 comment: Optional[pulumi.Input[pulumi.InputType['TableCommentArgs']]] = None,
                 default_time_to_live: Optional[pulumi.Input[int]] = None,
                 encryption_specification: Optional[pulumi.Input[pulumi.InputType['TableEncryptionSpecificationArgs']]] = None,
                 keyspace_name: Optional[pulumi.Input[str]] = None,
                 point_in_time_recovery: Optional[pulumi.Input[pulumi.InputType['TablePointInTimeRecoveryArgs']]] = None,
                 schema_definition: Optional[pulumi.Input[pulumi.InputType['TableSchemaDefinitionArgs']]] = None,
                 table_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ttl: Optional[pulumi.Input[pulumi.InputType['TableTtlArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TableArgs.__new__(TableArgs)

            __props__.__dict__["capacity_specification"] = capacity_specification
            __props__.__dict__["comment"] = comment
            __props__.__dict__["default_time_to_live"] = default_time_to_live
            __props__.__dict__["encryption_specification"] = encryption_specification
            if keyspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'keyspace_name'")
            __props__.__dict__["keyspace_name"] = keyspace_name
            __props__.__dict__["point_in_time_recovery"] = point_in_time_recovery
            if schema_definition is None and not opts.urn:
                raise TypeError("Missing required property 'schema_definition'")
            __props__.__dict__["schema_definition"] = schema_definition
            if table_name is None and not opts.urn:
                raise TypeError("Missing required property 'table_name'")
            __props__.__dict__["table_name"] = table_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["ttl"] = ttl
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(Table, __self__).__init__(
            'aws:keyspaces/table:Table',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            capacity_specification: Optional[pulumi.Input[pulumi.InputType['TableCapacitySpecificationArgs']]] = None,
            comment: Optional[pulumi.Input[pulumi.InputType['TableCommentArgs']]] = None,
            default_time_to_live: Optional[pulumi.Input[int]] = None,
            encryption_specification: Optional[pulumi.Input[pulumi.InputType['TableEncryptionSpecificationArgs']]] = None,
            keyspace_name: Optional[pulumi.Input[str]] = None,
            point_in_time_recovery: Optional[pulumi.Input[pulumi.InputType['TablePointInTimeRecoveryArgs']]] = None,
            schema_definition: Optional[pulumi.Input[pulumi.InputType['TableSchemaDefinitionArgs']]] = None,
            table_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            ttl: Optional[pulumi.Input[pulumi.InputType['TableTtlArgs']]] = None) -> 'Table':
        """
        Get an existing Table resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the table.
        :param pulumi.Input[pulumi.InputType['TableCapacitySpecificationArgs']] capacity_specification: Specifies the read/write throughput capacity mode for the table.
        :param pulumi.Input[pulumi.InputType['TableCommentArgs']] comment: A description of the table.
        :param pulumi.Input[int] default_time_to_live: The default Time to Live setting in seconds for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl).
        :param pulumi.Input[pulumi.InputType['TableEncryptionSpecificationArgs']] encryption_specification: Specifies how the encryption key for encryption at rest is managed for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html).
        :param pulumi.Input[str] keyspace_name: The name of the keyspace that the table is going to be created in.
        :param pulumi.Input[pulumi.InputType['TablePointInTimeRecoveryArgs']] point_in_time_recovery: Specifies if point-in-time recovery is enabled or disabled for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/PointInTimeRecovery.html).
        :param pulumi.Input[pulumi.InputType['TableSchemaDefinitionArgs']] schema_definition: Describes the schema of the table.
        :param pulumi.Input[str] table_name: The name of the table.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[pulumi.InputType['TableTtlArgs']] ttl: Enables Time to Live custom settings for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL.html).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TableState.__new__(_TableState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["capacity_specification"] = capacity_specification
        __props__.__dict__["comment"] = comment
        __props__.__dict__["default_time_to_live"] = default_time_to_live
        __props__.__dict__["encryption_specification"] = encryption_specification
        __props__.__dict__["keyspace_name"] = keyspace_name
        __props__.__dict__["point_in_time_recovery"] = point_in_time_recovery
        __props__.__dict__["schema_definition"] = schema_definition
        __props__.__dict__["table_name"] = table_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["ttl"] = ttl
        return Table(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the table.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="capacitySpecification")
    def capacity_specification(self) -> pulumi.Output['outputs.TableCapacitySpecification']:
        """
        Specifies the read/write throughput capacity mode for the table.
        """
        return pulumi.get(self, "capacity_specification")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output['outputs.TableComment']:
        """
        A description of the table.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="defaultTimeToLive")
    def default_time_to_live(self) -> pulumi.Output[Optional[int]]:
        """
        The default Time to Live setting in seconds for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL-how-it-works.html#ttl-howitworks_default_ttl).
        """
        return pulumi.get(self, "default_time_to_live")

    @property
    @pulumi.getter(name="encryptionSpecification")
    def encryption_specification(self) -> pulumi.Output['outputs.TableEncryptionSpecification']:
        """
        Specifies how the encryption key for encryption at rest is managed for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/EncryptionAtRest.html).
        """
        return pulumi.get(self, "encryption_specification")

    @property
    @pulumi.getter(name="keyspaceName")
    def keyspace_name(self) -> pulumi.Output[str]:
        """
        The name of the keyspace that the table is going to be created in.
        """
        return pulumi.get(self, "keyspace_name")

    @property
    @pulumi.getter(name="pointInTimeRecovery")
    def point_in_time_recovery(self) -> pulumi.Output['outputs.TablePointInTimeRecovery']:
        """
        Specifies if point-in-time recovery is enabled or disabled for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/PointInTimeRecovery.html).
        """
        return pulumi.get(self, "point_in_time_recovery")

    @property
    @pulumi.getter(name="schemaDefinition")
    def schema_definition(self) -> pulumi.Output['outputs.TableSchemaDefinition']:
        """
        Describes the schema of the table.
        """
        return pulumi.get(self, "schema_definition")

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> pulumi.Output[str]:
        """
        The name of the table.

        The following arguments are optional:
        """
        return pulumi.get(self, "table_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    def ttl(self) -> pulumi.Output[Optional['outputs.TableTtl']]:
        """
        Enables Time to Live custom settings for the table. More information can be found in the [Developer Guide](https://docs.aws.amazon.com/keyspaces/latest/devguide/TTL.html).
        """
        return pulumi.get(self, "ttl")

