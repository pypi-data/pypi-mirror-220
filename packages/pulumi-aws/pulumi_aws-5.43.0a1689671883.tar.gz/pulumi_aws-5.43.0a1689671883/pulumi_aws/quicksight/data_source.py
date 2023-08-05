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

__all__ = ['DataSourceArgs', 'DataSource']

@pulumi.input_type
class DataSourceArgs:
    def __init__(__self__, *,
                 data_source_id: pulumi.Input[str],
                 parameters: pulumi.Input['DataSourceParametersArgs'],
                 type: pulumi.Input[str],
                 aws_account_id: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input['DataSourceCredentialsArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input['DataSourcePermissionArgs']]]] = None,
                 ssl_properties: Optional[pulumi.Input['DataSourceSslPropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vpc_connection_properties: Optional[pulumi.Input['DataSourceVpcConnectionPropertiesArgs']] = None):
        """
        The set of arguments for constructing a DataSource resource.
        :param pulumi.Input[str] data_source_id: An identifier for the data source.
        :param pulumi.Input['DataSourceParametersArgs'] parameters: The parameters used to connect to this data source (exactly one).
        :param pulumi.Input[str] type: The type of the data source. See the [AWS Documentation](https://docs.aws.amazon.com/quicksight/latest/APIReference/API_CreateDataSource.html#QS-CreateDataSource-request-Type) for the complete list of valid values.
               
               The following arguments are optional:
        :param pulumi.Input[str] aws_account_id: The ID for the AWS account that the data source is in. Currently, you use the ID for the AWS account that contains your Amazon QuickSight account.
        :param pulumi.Input['DataSourceCredentialsArgs'] credentials: The credentials Amazon QuickSight uses to connect to your underlying source. Currently, only credentials based on user name and password are supported. See Credentials below for more details.
        :param pulumi.Input[str] name: A name for the data source, maximum of 128 characters.
        :param pulumi.Input[Sequence[pulumi.Input['DataSourcePermissionArgs']]] permissions: A set of resource permissions on the data source. Maximum of 64 items. See Permission below for more details.
        :param pulumi.Input['DataSourceSslPropertiesArgs'] ssl_properties: Secure Socket Layer (SSL) properties that apply when Amazon QuickSight connects to your underlying source. See SSL Properties below for more details.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input['DataSourceVpcConnectionPropertiesArgs'] vpc_connection_properties: Use this parameter only when you want Amazon QuickSight to use a VPC connection when connecting to your underlying source. See VPC Connection Properties below for more details.
        """
        pulumi.set(__self__, "data_source_id", data_source_id)
        pulumi.set(__self__, "parameters", parameters)
        pulumi.set(__self__, "type", type)
        if aws_account_id is not None:
            pulumi.set(__self__, "aws_account_id", aws_account_id)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if permissions is not None:
            pulumi.set(__self__, "permissions", permissions)
        if ssl_properties is not None:
            pulumi.set(__self__, "ssl_properties", ssl_properties)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vpc_connection_properties is not None:
            pulumi.set(__self__, "vpc_connection_properties", vpc_connection_properties)

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> pulumi.Input[str]:
        """
        An identifier for the data source.
        """
        return pulumi.get(self, "data_source_id")

    @data_source_id.setter
    def data_source_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_source_id", value)

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Input['DataSourceParametersArgs']:
        """
        The parameters used to connect to this data source (exactly one).
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: pulumi.Input['DataSourceParametersArgs']):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of the data source. See the [AWS Documentation](https://docs.aws.amazon.com/quicksight/latest/APIReference/API_CreateDataSource.html#QS-CreateDataSource-request-Type) for the complete list of valid values.

        The following arguments are optional:
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID for the AWS account that the data source is in. Currently, you use the ID for the AWS account that contains your Amazon QuickSight account.
        """
        return pulumi.get(self, "aws_account_id")

    @aws_account_id.setter
    def aws_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_account_id", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['DataSourceCredentialsArgs']]:
        """
        The credentials Amazon QuickSight uses to connect to your underlying source. Currently, only credentials based on user name and password are supported. See Credentials below for more details.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['DataSourceCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the data source, maximum of 128 characters.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def permissions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DataSourcePermissionArgs']]]]:
        """
        A set of resource permissions on the data source. Maximum of 64 items. See Permission below for more details.
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DataSourcePermissionArgs']]]]):
        pulumi.set(self, "permissions", value)

    @property
    @pulumi.getter(name="sslProperties")
    def ssl_properties(self) -> Optional[pulumi.Input['DataSourceSslPropertiesArgs']]:
        """
        Secure Socket Layer (SSL) properties that apply when Amazon QuickSight connects to your underlying source. See SSL Properties below for more details.
        """
        return pulumi.get(self, "ssl_properties")

    @ssl_properties.setter
    def ssl_properties(self, value: Optional[pulumi.Input['DataSourceSslPropertiesArgs']]):
        pulumi.set(self, "ssl_properties", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vpcConnectionProperties")
    def vpc_connection_properties(self) -> Optional[pulumi.Input['DataSourceVpcConnectionPropertiesArgs']]:
        """
        Use this parameter only when you want Amazon QuickSight to use a VPC connection when connecting to your underlying source. See VPC Connection Properties below for more details.
        """
        return pulumi.get(self, "vpc_connection_properties")

    @vpc_connection_properties.setter
    def vpc_connection_properties(self, value: Optional[pulumi.Input['DataSourceVpcConnectionPropertiesArgs']]):
        pulumi.set(self, "vpc_connection_properties", value)


@pulumi.input_type
class _DataSourceState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 aws_account_id: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input['DataSourceCredentialsArgs']] = None,
                 data_source_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input['DataSourceParametersArgs']] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input['DataSourcePermissionArgs']]]] = None,
                 ssl_properties: Optional[pulumi.Input['DataSourceSslPropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 vpc_connection_properties: Optional[pulumi.Input['DataSourceVpcConnectionPropertiesArgs']] = None):
        """
        Input properties used for looking up and filtering DataSource resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the data source
        :param pulumi.Input[str] aws_account_id: The ID for the AWS account that the data source is in. Currently, you use the ID for the AWS account that contains your Amazon QuickSight account.
        :param pulumi.Input['DataSourceCredentialsArgs'] credentials: The credentials Amazon QuickSight uses to connect to your underlying source. Currently, only credentials based on user name and password are supported. See Credentials below for more details.
        :param pulumi.Input[str] data_source_id: An identifier for the data source.
        :param pulumi.Input[str] name: A name for the data source, maximum of 128 characters.
        :param pulumi.Input['DataSourceParametersArgs'] parameters: The parameters used to connect to this data source (exactly one).
        :param pulumi.Input[Sequence[pulumi.Input['DataSourcePermissionArgs']]] permissions: A set of resource permissions on the data source. Maximum of 64 items. See Permission below for more details.
        :param pulumi.Input['DataSourceSslPropertiesArgs'] ssl_properties: Secure Socket Layer (SSL) properties that apply when Amazon QuickSight connects to your underlying source. See SSL Properties below for more details.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] type: The type of the data source. See the [AWS Documentation](https://docs.aws.amazon.com/quicksight/latest/APIReference/API_CreateDataSource.html#QS-CreateDataSource-request-Type) for the complete list of valid values.
               
               The following arguments are optional:
        :param pulumi.Input['DataSourceVpcConnectionPropertiesArgs'] vpc_connection_properties: Use this parameter only when you want Amazon QuickSight to use a VPC connection when connecting to your underlying source. See VPC Connection Properties below for more details.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if aws_account_id is not None:
            pulumi.set(__self__, "aws_account_id", aws_account_id)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if data_source_id is not None:
            pulumi.set(__self__, "data_source_id", data_source_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if permissions is not None:
            pulumi.set(__self__, "permissions", permissions)
        if ssl_properties is not None:
            pulumi.set(__self__, "ssl_properties", ssl_properties)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if vpc_connection_properties is not None:
            pulumi.set(__self__, "vpc_connection_properties", vpc_connection_properties)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the data source
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID for the AWS account that the data source is in. Currently, you use the ID for the AWS account that contains your Amazon QuickSight account.
        """
        return pulumi.get(self, "aws_account_id")

    @aws_account_id.setter
    def aws_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_account_id", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['DataSourceCredentialsArgs']]:
        """
        The credentials Amazon QuickSight uses to connect to your underlying source. Currently, only credentials based on user name and password are supported. See Credentials below for more details.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['DataSourceCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> Optional[pulumi.Input[str]]:
        """
        An identifier for the data source.
        """
        return pulumi.get(self, "data_source_id")

    @data_source_id.setter
    def data_source_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_source_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the data source, maximum of 128 characters.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input['DataSourceParametersArgs']]:
        """
        The parameters used to connect to this data source (exactly one).
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input['DataSourceParametersArgs']]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter
    def permissions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DataSourcePermissionArgs']]]]:
        """
        A set of resource permissions on the data source. Maximum of 64 items. See Permission below for more details.
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DataSourcePermissionArgs']]]]):
        pulumi.set(self, "permissions", value)

    @property
    @pulumi.getter(name="sslProperties")
    def ssl_properties(self) -> Optional[pulumi.Input['DataSourceSslPropertiesArgs']]:
        """
        Secure Socket Layer (SSL) properties that apply when Amazon QuickSight connects to your underlying source. See SSL Properties below for more details.
        """
        return pulumi.get(self, "ssl_properties")

    @ssl_properties.setter
    def ssl_properties(self, value: Optional[pulumi.Input['DataSourceSslPropertiesArgs']]):
        pulumi.set(self, "ssl_properties", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the data source. See the [AWS Documentation](https://docs.aws.amazon.com/quicksight/latest/APIReference/API_CreateDataSource.html#QS-CreateDataSource-request-Type) for the complete list of valid values.

        The following arguments are optional:
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="vpcConnectionProperties")
    def vpc_connection_properties(self) -> Optional[pulumi.Input['DataSourceVpcConnectionPropertiesArgs']]:
        """
        Use this parameter only when you want Amazon QuickSight to use a VPC connection when connecting to your underlying source. See VPC Connection Properties below for more details.
        """
        return pulumi.get(self, "vpc_connection_properties")

    @vpc_connection_properties.setter
    def vpc_connection_properties(self, value: Optional[pulumi.Input['DataSourceVpcConnectionPropertiesArgs']]):
        pulumi.set(self, "vpc_connection_properties", value)


class DataSource(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws_account_id: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input[pulumi.InputType['DataSourceCredentialsArgs']]] = None,
                 data_source_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[pulumi.InputType['DataSourceParametersArgs']]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataSourcePermissionArgs']]]]] = None,
                 ssl_properties: Optional[pulumi.Input[pulumi.InputType['DataSourceSslPropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 vpc_connection_properties: Optional[pulumi.Input[pulumi.InputType['DataSourceVpcConnectionPropertiesArgs']]] = None,
                 __props__=None):
        """
        Resource for managing QuickSight Data Source

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default = aws.quicksight.DataSource("default",
            data_source_id="example-id",
            parameters=aws.quicksight.DataSourceParametersArgs(
                s3=aws.quicksight.DataSourceParametersS3Args(
                    manifest_file_location=aws.quicksight.DataSourceParametersS3ManifestFileLocationArgs(
                        bucket="my-bucket",
                        key="path/to/manifest.json",
                    ),
                ),
            ),
            type="S3")
        ```

        ## Import

        A QuickSight data source can be imported using the AWS account ID, and data source ID separated by a slash (`/`) e.g.,

        ```sh
         $ pulumi import aws:quicksight/dataSource:DataSource example 123456789123/my-data-source-id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] aws_account_id: The ID for the AWS account that the data source is in. Currently, you use the ID for the AWS account that contains your Amazon QuickSight account.
        :param pulumi.Input[pulumi.InputType['DataSourceCredentialsArgs']] credentials: The credentials Amazon QuickSight uses to connect to your underlying source. Currently, only credentials based on user name and password are supported. See Credentials below for more details.
        :param pulumi.Input[str] data_source_id: An identifier for the data source.
        :param pulumi.Input[str] name: A name for the data source, maximum of 128 characters.
        :param pulumi.Input[pulumi.InputType['DataSourceParametersArgs']] parameters: The parameters used to connect to this data source (exactly one).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataSourcePermissionArgs']]]] permissions: A set of resource permissions on the data source. Maximum of 64 items. See Permission below for more details.
        :param pulumi.Input[pulumi.InputType['DataSourceSslPropertiesArgs']] ssl_properties: Secure Socket Layer (SSL) properties that apply when Amazon QuickSight connects to your underlying source. See SSL Properties below for more details.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: The type of the data source. See the [AWS Documentation](https://docs.aws.amazon.com/quicksight/latest/APIReference/API_CreateDataSource.html#QS-CreateDataSource-request-Type) for the complete list of valid values.
               
               The following arguments are optional:
        :param pulumi.Input[pulumi.InputType['DataSourceVpcConnectionPropertiesArgs']] vpc_connection_properties: Use this parameter only when you want Amazon QuickSight to use a VPC connection when connecting to your underlying source. See VPC Connection Properties below for more details.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DataSourceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing QuickSight Data Source

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default = aws.quicksight.DataSource("default",
            data_source_id="example-id",
            parameters=aws.quicksight.DataSourceParametersArgs(
                s3=aws.quicksight.DataSourceParametersS3Args(
                    manifest_file_location=aws.quicksight.DataSourceParametersS3ManifestFileLocationArgs(
                        bucket="my-bucket",
                        key="path/to/manifest.json",
                    ),
                ),
            ),
            type="S3")
        ```

        ## Import

        A QuickSight data source can be imported using the AWS account ID, and data source ID separated by a slash (`/`) e.g.,

        ```sh
         $ pulumi import aws:quicksight/dataSource:DataSource example 123456789123/my-data-source-id
        ```

        :param str resource_name: The name of the resource.
        :param DataSourceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DataSourceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws_account_id: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input[pulumi.InputType['DataSourceCredentialsArgs']]] = None,
                 data_source_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[pulumi.InputType['DataSourceParametersArgs']]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataSourcePermissionArgs']]]]] = None,
                 ssl_properties: Optional[pulumi.Input[pulumi.InputType['DataSourceSslPropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 vpc_connection_properties: Optional[pulumi.Input[pulumi.InputType['DataSourceVpcConnectionPropertiesArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DataSourceArgs.__new__(DataSourceArgs)

            __props__.__dict__["aws_account_id"] = aws_account_id
            __props__.__dict__["credentials"] = credentials
            if data_source_id is None and not opts.urn:
                raise TypeError("Missing required property 'data_source_id'")
            __props__.__dict__["data_source_id"] = data_source_id
            __props__.__dict__["name"] = name
            if parameters is None and not opts.urn:
                raise TypeError("Missing required property 'parameters'")
            __props__.__dict__["parameters"] = parameters
            __props__.__dict__["permissions"] = permissions
            __props__.__dict__["ssl_properties"] = ssl_properties
            __props__.__dict__["tags"] = tags
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["vpc_connection_properties"] = vpc_connection_properties
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(DataSource, __self__).__init__(
            'aws:quicksight/dataSource:DataSource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            aws_account_id: Optional[pulumi.Input[str]] = None,
            credentials: Optional[pulumi.Input[pulumi.InputType['DataSourceCredentialsArgs']]] = None,
            data_source_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            parameters: Optional[pulumi.Input[pulumi.InputType['DataSourceParametersArgs']]] = None,
            permissions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataSourcePermissionArgs']]]]] = None,
            ssl_properties: Optional[pulumi.Input[pulumi.InputType['DataSourceSslPropertiesArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            type: Optional[pulumi.Input[str]] = None,
            vpc_connection_properties: Optional[pulumi.Input[pulumi.InputType['DataSourceVpcConnectionPropertiesArgs']]] = None) -> 'DataSource':
        """
        Get an existing DataSource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the data source
        :param pulumi.Input[str] aws_account_id: The ID for the AWS account that the data source is in. Currently, you use the ID for the AWS account that contains your Amazon QuickSight account.
        :param pulumi.Input[pulumi.InputType['DataSourceCredentialsArgs']] credentials: The credentials Amazon QuickSight uses to connect to your underlying source. Currently, only credentials based on user name and password are supported. See Credentials below for more details.
        :param pulumi.Input[str] data_source_id: An identifier for the data source.
        :param pulumi.Input[str] name: A name for the data source, maximum of 128 characters.
        :param pulumi.Input[pulumi.InputType['DataSourceParametersArgs']] parameters: The parameters used to connect to this data source (exactly one).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataSourcePermissionArgs']]]] permissions: A set of resource permissions on the data source. Maximum of 64 items. See Permission below for more details.
        :param pulumi.Input[pulumi.InputType['DataSourceSslPropertiesArgs']] ssl_properties: Secure Socket Layer (SSL) properties that apply when Amazon QuickSight connects to your underlying source. See SSL Properties below for more details.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] type: The type of the data source. See the [AWS Documentation](https://docs.aws.amazon.com/quicksight/latest/APIReference/API_CreateDataSource.html#QS-CreateDataSource-request-Type) for the complete list of valid values.
               
               The following arguments are optional:
        :param pulumi.Input[pulumi.InputType['DataSourceVpcConnectionPropertiesArgs']] vpc_connection_properties: Use this parameter only when you want Amazon QuickSight to use a VPC connection when connecting to your underlying source. See VPC Connection Properties below for more details.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DataSourceState.__new__(_DataSourceState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["aws_account_id"] = aws_account_id
        __props__.__dict__["credentials"] = credentials
        __props__.__dict__["data_source_id"] = data_source_id
        __props__.__dict__["name"] = name
        __props__.__dict__["parameters"] = parameters
        __props__.__dict__["permissions"] = permissions
        __props__.__dict__["ssl_properties"] = ssl_properties
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["type"] = type
        __props__.__dict__["vpc_connection_properties"] = vpc_connection_properties
        return DataSource(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the data source
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> pulumi.Output[str]:
        """
        The ID for the AWS account that the data source is in. Currently, you use the ID for the AWS account that contains your Amazon QuickSight account.
        """
        return pulumi.get(self, "aws_account_id")

    @property
    @pulumi.getter
    def credentials(self) -> pulumi.Output[Optional['outputs.DataSourceCredentials']]:
        """
        The credentials Amazon QuickSight uses to connect to your underlying source. Currently, only credentials based on user name and password are supported. See Credentials below for more details.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> pulumi.Output[str]:
        """
        An identifier for the data source.
        """
        return pulumi.get(self, "data_source_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A name for the data source, maximum of 128 characters.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output['outputs.DataSourceParameters']:
        """
        The parameters used to connect to this data source (exactly one).
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter
    def permissions(self) -> pulumi.Output[Optional[Sequence['outputs.DataSourcePermission']]]:
        """
        A set of resource permissions on the data source. Maximum of 64 items. See Permission below for more details.
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter(name="sslProperties")
    def ssl_properties(self) -> pulumi.Output[Optional['outputs.DataSourceSslProperties']]:
        """
        Secure Socket Layer (SSL) properties that apply when Amazon QuickSight connects to your underlying source. See SSL Properties below for more details.
        """
        return pulumi.get(self, "ssl_properties")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    def type(self) -> pulumi.Output[str]:
        """
        The type of the data source. See the [AWS Documentation](https://docs.aws.amazon.com/quicksight/latest/APIReference/API_CreateDataSource.html#QS-CreateDataSource-request-Type) for the complete list of valid values.

        The following arguments are optional:
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vpcConnectionProperties")
    def vpc_connection_properties(self) -> pulumi.Output[Optional['outputs.DataSourceVpcConnectionProperties']]:
        """
        Use this parameter only when you want Amazon QuickSight to use a VPC connection when connecting to your underlying source. See VPC Connection Properties below for more details.
        """
        return pulumi.get(self, "vpc_connection_properties")

