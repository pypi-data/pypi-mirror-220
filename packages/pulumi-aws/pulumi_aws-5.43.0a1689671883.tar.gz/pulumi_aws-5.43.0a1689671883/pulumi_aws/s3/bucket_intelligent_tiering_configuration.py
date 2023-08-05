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

__all__ = ['BucketIntelligentTieringConfigurationArgs', 'BucketIntelligentTieringConfiguration']

@pulumi.input_type
class BucketIntelligentTieringConfigurationArgs:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 tierings: pulumi.Input[Sequence[pulumi.Input['BucketIntelligentTieringConfigurationTieringArgs']]],
                 filter: Optional[pulumi.Input['BucketIntelligentTieringConfigurationFilterArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BucketIntelligentTieringConfiguration resource.
        :param pulumi.Input[str] bucket: Name of the bucket this intelligent tiering configuration is associated with.
        :param pulumi.Input[Sequence[pulumi.Input['BucketIntelligentTieringConfigurationTieringArgs']]] tierings: S3 Intelligent-Tiering storage class tiers of the configuration (documented below).
        :param pulumi.Input['BucketIntelligentTieringConfigurationFilterArgs'] filter: Bucket filter. The configuration only includes objects that meet the filter's criteria (documented below).
        :param pulumi.Input[str] name: Unique name used to identify the S3 Intelligent-Tiering configuration for the bucket.
        :param pulumi.Input[str] status: Specifies the status of the configuration. Valid values: `Enabled`, `Disabled`.
        """
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "tierings", tierings)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        Name of the bucket this intelligent tiering configuration is associated with.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def tierings(self) -> pulumi.Input[Sequence[pulumi.Input['BucketIntelligentTieringConfigurationTieringArgs']]]:
        """
        S3 Intelligent-Tiering storage class tiers of the configuration (documented below).
        """
        return pulumi.get(self, "tierings")

    @tierings.setter
    def tierings(self, value: pulumi.Input[Sequence[pulumi.Input['BucketIntelligentTieringConfigurationTieringArgs']]]):
        pulumi.set(self, "tierings", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['BucketIntelligentTieringConfigurationFilterArgs']]:
        """
        Bucket filter. The configuration only includes objects that meet the filter's criteria (documented below).
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['BucketIntelligentTieringConfigurationFilterArgs']]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique name used to identify the S3 Intelligent-Tiering configuration for the bucket.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the status of the configuration. Valid values: `Enabled`, `Disabled`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _BucketIntelligentTieringConfigurationState:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input['BucketIntelligentTieringConfigurationFilterArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tierings: Optional[pulumi.Input[Sequence[pulumi.Input['BucketIntelligentTieringConfigurationTieringArgs']]]] = None):
        """
        Input properties used for looking up and filtering BucketIntelligentTieringConfiguration resources.
        :param pulumi.Input[str] bucket: Name of the bucket this intelligent tiering configuration is associated with.
        :param pulumi.Input['BucketIntelligentTieringConfigurationFilterArgs'] filter: Bucket filter. The configuration only includes objects that meet the filter's criteria (documented below).
        :param pulumi.Input[str] name: Unique name used to identify the S3 Intelligent-Tiering configuration for the bucket.
        :param pulumi.Input[str] status: Specifies the status of the configuration. Valid values: `Enabled`, `Disabled`.
        :param pulumi.Input[Sequence[pulumi.Input['BucketIntelligentTieringConfigurationTieringArgs']]] tierings: S3 Intelligent-Tiering storage class tiers of the configuration (documented below).
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tierings is not None:
            pulumi.set(__self__, "tierings", tierings)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the bucket this intelligent tiering configuration is associated with.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['BucketIntelligentTieringConfigurationFilterArgs']]:
        """
        Bucket filter. The configuration only includes objects that meet the filter's criteria (documented below).
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['BucketIntelligentTieringConfigurationFilterArgs']]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique name used to identify the S3 Intelligent-Tiering configuration for the bucket.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the status of the configuration. Valid values: `Enabled`, `Disabled`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tierings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BucketIntelligentTieringConfigurationTieringArgs']]]]:
        """
        S3 Intelligent-Tiering storage class tiers of the configuration (documented below).
        """
        return pulumi.get(self, "tierings")

    @tierings.setter
    def tierings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BucketIntelligentTieringConfigurationTieringArgs']]]]):
        pulumi.set(self, "tierings", value)


class BucketIntelligentTieringConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationFilterArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tierings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationTieringArgs']]]]] = None,
                 __props__=None):
        """
        Provides an [S3 Intelligent-Tiering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering.html) configuration resource.

        ## Example Usage
        ### Add intelligent tiering configuration for entire S3 bucket

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example")
        example_entire_bucket = aws.s3.BucketIntelligentTieringConfiguration("example-entire-bucket",
            bucket=example.id,
            tierings=[
                aws.s3.BucketIntelligentTieringConfigurationTieringArgs(
                    access_tier="DEEP_ARCHIVE_ACCESS",
                    days=180,
                ),
                aws.s3.BucketIntelligentTieringConfigurationTieringArgs(
                    access_tier="ARCHIVE_ACCESS",
                    days=125,
                ),
            ])
        ```
        ### Add intelligent tiering configuration with S3 object filter

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example")
        example_filtered = aws.s3.BucketIntelligentTieringConfiguration("example-filtered",
            bucket=example.id,
            status="Disabled",
            filter=aws.s3.BucketIntelligentTieringConfigurationFilterArgs(
                prefix="documents/",
                tags={
                    "priority": "high",
                    "class": "blue",
                },
            ),
            tierings=[aws.s3.BucketIntelligentTieringConfigurationTieringArgs(
                access_tier="ARCHIVE_ACCESS",
                days=125,
            )])
        ```

        ## Import

        S3 bucket intelligent tiering configurations can be imported using `bucket:name`, e.g.

        ```sh
         $ pulumi import aws:s3/bucketIntelligentTieringConfiguration:BucketIntelligentTieringConfiguration my-bucket-entire-bucket my-bucket:EntireBucket
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the bucket this intelligent tiering configuration is associated with.
        :param pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationFilterArgs']] filter: Bucket filter. The configuration only includes objects that meet the filter's criteria (documented below).
        :param pulumi.Input[str] name: Unique name used to identify the S3 Intelligent-Tiering configuration for the bucket.
        :param pulumi.Input[str] status: Specifies the status of the configuration. Valid values: `Enabled`, `Disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationTieringArgs']]]] tierings: S3 Intelligent-Tiering storage class tiers of the configuration (documented below).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketIntelligentTieringConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an [S3 Intelligent-Tiering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering.html) configuration resource.

        ## Example Usage
        ### Add intelligent tiering configuration for entire S3 bucket

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example")
        example_entire_bucket = aws.s3.BucketIntelligentTieringConfiguration("example-entire-bucket",
            bucket=example.id,
            tierings=[
                aws.s3.BucketIntelligentTieringConfigurationTieringArgs(
                    access_tier="DEEP_ARCHIVE_ACCESS",
                    days=180,
                ),
                aws.s3.BucketIntelligentTieringConfigurationTieringArgs(
                    access_tier="ARCHIVE_ACCESS",
                    days=125,
                ),
            ])
        ```
        ### Add intelligent tiering configuration with S3 object filter

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example")
        example_filtered = aws.s3.BucketIntelligentTieringConfiguration("example-filtered",
            bucket=example.id,
            status="Disabled",
            filter=aws.s3.BucketIntelligentTieringConfigurationFilterArgs(
                prefix="documents/",
                tags={
                    "priority": "high",
                    "class": "blue",
                },
            ),
            tierings=[aws.s3.BucketIntelligentTieringConfigurationTieringArgs(
                access_tier="ARCHIVE_ACCESS",
                days=125,
            )])
        ```

        ## Import

        S3 bucket intelligent tiering configurations can be imported using `bucket:name`, e.g.

        ```sh
         $ pulumi import aws:s3/bucketIntelligentTieringConfiguration:BucketIntelligentTieringConfiguration my-bucket-entire-bucket my-bucket:EntireBucket
        ```

        :param str resource_name: The name of the resource.
        :param BucketIntelligentTieringConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketIntelligentTieringConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationFilterArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tierings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationTieringArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketIntelligentTieringConfigurationArgs.__new__(BucketIntelligentTieringConfigurationArgs)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            __props__.__dict__["filter"] = filter
            __props__.__dict__["name"] = name
            __props__.__dict__["status"] = status
            if tierings is None and not opts.urn:
                raise TypeError("Missing required property 'tierings'")
            __props__.__dict__["tierings"] = tierings
        super(BucketIntelligentTieringConfiguration, __self__).__init__(
            'aws:s3/bucketIntelligentTieringConfiguration:BucketIntelligentTieringConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            filter: Optional[pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationFilterArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tierings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationTieringArgs']]]]] = None) -> 'BucketIntelligentTieringConfiguration':
        """
        Get an existing BucketIntelligentTieringConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the bucket this intelligent tiering configuration is associated with.
        :param pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationFilterArgs']] filter: Bucket filter. The configuration only includes objects that meet the filter's criteria (documented below).
        :param pulumi.Input[str] name: Unique name used to identify the S3 Intelligent-Tiering configuration for the bucket.
        :param pulumi.Input[str] status: Specifies the status of the configuration. Valid values: `Enabled`, `Disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketIntelligentTieringConfigurationTieringArgs']]]] tierings: S3 Intelligent-Tiering storage class tiers of the configuration (documented below).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BucketIntelligentTieringConfigurationState.__new__(_BucketIntelligentTieringConfigurationState)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["filter"] = filter
        __props__.__dict__["name"] = name
        __props__.__dict__["status"] = status
        __props__.__dict__["tierings"] = tierings
        return BucketIntelligentTieringConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        Name of the bucket this intelligent tiering configuration is associated with.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Output[Optional['outputs.BucketIntelligentTieringConfigurationFilter']]:
        """
        Bucket filter. The configuration only includes objects that meet the filter's criteria (documented below).
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Unique name used to identify the S3 Intelligent-Tiering configuration for the bucket.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the status of the configuration. Valid values: `Enabled`, `Disabled`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tierings(self) -> pulumi.Output[Sequence['outputs.BucketIntelligentTieringConfigurationTiering']]:
        """
        S3 Intelligent-Tiering storage class tiers of the configuration (documented below).
        """
        return pulumi.get(self, "tierings")

