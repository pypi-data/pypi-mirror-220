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

__all__ = ['BucketLoggingV2Args', 'BucketLoggingV2']

@pulumi.input_type
class BucketLoggingV2Args:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 target_bucket: pulumi.Input[str],
                 target_prefix: pulumi.Input[str],
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 target_grants: Optional[pulumi.Input[Sequence[pulumi.Input['BucketLoggingV2TargetGrantArgs']]]] = None):
        """
        The set of arguments for constructing a BucketLoggingV2 resource.
        :param pulumi.Input[str] bucket: Name of the bucket.
        :param pulumi.Input[str] target_bucket: Name of the bucket where you want Amazon S3 to store server access logs.
        :param pulumi.Input[str] target_prefix: Prefix for all log object keys.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner.
        :param pulumi.Input[Sequence[pulumi.Input['BucketLoggingV2TargetGrantArgs']]] target_grants: Set of configuration blocks with information for granting permissions. See below.
        """
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "target_bucket", target_bucket)
        pulumi.set(__self__, "target_prefix", target_prefix)
        if expected_bucket_owner is not None:
            pulumi.set(__self__, "expected_bucket_owner", expected_bucket_owner)
        if target_grants is not None:
            pulumi.set(__self__, "target_grants", target_grants)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        Name of the bucket.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="targetBucket")
    def target_bucket(self) -> pulumi.Input[str]:
        """
        Name of the bucket where you want Amazon S3 to store server access logs.
        """
        return pulumi.get(self, "target_bucket")

    @target_bucket.setter
    def target_bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_bucket", value)

    @property
    @pulumi.getter(name="targetPrefix")
    def target_prefix(self) -> pulumi.Input[str]:
        """
        Prefix for all log object keys.
        """
        return pulumi.get(self, "target_prefix")

    @target_prefix.setter
    def target_prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_prefix", value)

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> Optional[pulumi.Input[str]]:
        """
        Account ID of the expected bucket owner.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expected_bucket_owner", value)

    @property
    @pulumi.getter(name="targetGrants")
    def target_grants(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BucketLoggingV2TargetGrantArgs']]]]:
        """
        Set of configuration blocks with information for granting permissions. See below.
        """
        return pulumi.get(self, "target_grants")

    @target_grants.setter
    def target_grants(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BucketLoggingV2TargetGrantArgs']]]]):
        pulumi.set(self, "target_grants", value)


@pulumi.input_type
class _BucketLoggingV2State:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 target_bucket: Optional[pulumi.Input[str]] = None,
                 target_grants: Optional[pulumi.Input[Sequence[pulumi.Input['BucketLoggingV2TargetGrantArgs']]]] = None,
                 target_prefix: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BucketLoggingV2 resources.
        :param pulumi.Input[str] bucket: Name of the bucket.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner.
        :param pulumi.Input[str] target_bucket: Name of the bucket where you want Amazon S3 to store server access logs.
        :param pulumi.Input[Sequence[pulumi.Input['BucketLoggingV2TargetGrantArgs']]] target_grants: Set of configuration blocks with information for granting permissions. See below.
        :param pulumi.Input[str] target_prefix: Prefix for all log object keys.
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if expected_bucket_owner is not None:
            pulumi.set(__self__, "expected_bucket_owner", expected_bucket_owner)
        if target_bucket is not None:
            pulumi.set(__self__, "target_bucket", target_bucket)
        if target_grants is not None:
            pulumi.set(__self__, "target_grants", target_grants)
        if target_prefix is not None:
            pulumi.set(__self__, "target_prefix", target_prefix)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the bucket.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> Optional[pulumi.Input[str]]:
        """
        Account ID of the expected bucket owner.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expected_bucket_owner", value)

    @property
    @pulumi.getter(name="targetBucket")
    def target_bucket(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the bucket where you want Amazon S3 to store server access logs.
        """
        return pulumi.get(self, "target_bucket")

    @target_bucket.setter
    def target_bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_bucket", value)

    @property
    @pulumi.getter(name="targetGrants")
    def target_grants(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BucketLoggingV2TargetGrantArgs']]]]:
        """
        Set of configuration blocks with information for granting permissions. See below.
        """
        return pulumi.get(self, "target_grants")

    @target_grants.setter
    def target_grants(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BucketLoggingV2TargetGrantArgs']]]]):
        pulumi.set(self, "target_grants", value)

    @property
    @pulumi.getter(name="targetPrefix")
    def target_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Prefix for all log object keys.
        """
        return pulumi.get(self, "target_prefix")

    @target_prefix.setter
    def target_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_prefix", value)


class BucketLoggingV2(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 target_bucket: Optional[pulumi.Input[str]] = None,
                 target_grants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLoggingV2TargetGrantArgs']]]]] = None,
                 target_prefix: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an S3 bucket (server access) logging resource. For more information, see [Logging requests using server access logging](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html)
        in the AWS S3 User Guide.

        > **Note:** Amazon S3 supports server access logging, AWS CloudTrail, or a combination of both. Refer to the [Logging options for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/logging-with-S3.html)
        to decide which method meets your requirements.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_bucket_v2 = aws.s3.BucketV2("exampleBucketV2")
        example_bucket_acl_v2 = aws.s3.BucketAclV2("exampleBucketAclV2",
            bucket=example_bucket_v2.id,
            acl="private")
        log_bucket = aws.s3.BucketV2("logBucket")
        log_bucket_acl = aws.s3.BucketAclV2("logBucketAcl",
            bucket=log_bucket.id,
            acl="log-delivery-write")
        example_bucket_logging_v2 = aws.s3.BucketLoggingV2("exampleBucketLoggingV2",
            bucket=example_bucket_v2.id,
            target_bucket=log_bucket.id,
            target_prefix="log/")
        ```

        ## Import

        S3 bucket logging can be imported in one of two ways. If the owner (account ID) of the source bucket is the same account used to configure the AWS Provider, the S3 bucket logging resource should be imported using the `bucket` e.g.,

        ```sh
         $ pulumi import aws:s3/bucketLoggingV2:BucketLoggingV2 example bucket-name
        ```

         If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, the S3 bucket logging resource should be imported using the `bucket` and `expected_bucket_owner` separated by a comma (`,`) e.g.,

        ```sh
         $ pulumi import aws:s3/bucketLoggingV2:BucketLoggingV2 example bucket-name,123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the bucket.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner.
        :param pulumi.Input[str] target_bucket: Name of the bucket where you want Amazon S3 to store server access logs.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLoggingV2TargetGrantArgs']]]] target_grants: Set of configuration blocks with information for granting permissions. See below.
        :param pulumi.Input[str] target_prefix: Prefix for all log object keys.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketLoggingV2Args,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an S3 bucket (server access) logging resource. For more information, see [Logging requests using server access logging](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html)
        in the AWS S3 User Guide.

        > **Note:** Amazon S3 supports server access logging, AWS CloudTrail, or a combination of both. Refer to the [Logging options for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/logging-with-S3.html)
        to decide which method meets your requirements.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_bucket_v2 = aws.s3.BucketV2("exampleBucketV2")
        example_bucket_acl_v2 = aws.s3.BucketAclV2("exampleBucketAclV2",
            bucket=example_bucket_v2.id,
            acl="private")
        log_bucket = aws.s3.BucketV2("logBucket")
        log_bucket_acl = aws.s3.BucketAclV2("logBucketAcl",
            bucket=log_bucket.id,
            acl="log-delivery-write")
        example_bucket_logging_v2 = aws.s3.BucketLoggingV2("exampleBucketLoggingV2",
            bucket=example_bucket_v2.id,
            target_bucket=log_bucket.id,
            target_prefix="log/")
        ```

        ## Import

        S3 bucket logging can be imported in one of two ways. If the owner (account ID) of the source bucket is the same account used to configure the AWS Provider, the S3 bucket logging resource should be imported using the `bucket` e.g.,

        ```sh
         $ pulumi import aws:s3/bucketLoggingV2:BucketLoggingV2 example bucket-name
        ```

         If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, the S3 bucket logging resource should be imported using the `bucket` and `expected_bucket_owner` separated by a comma (`,`) e.g.,

        ```sh
         $ pulumi import aws:s3/bucketLoggingV2:BucketLoggingV2 example bucket-name,123456789012
        ```

        :param str resource_name: The name of the resource.
        :param BucketLoggingV2Args args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketLoggingV2Args, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 target_bucket: Optional[pulumi.Input[str]] = None,
                 target_grants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLoggingV2TargetGrantArgs']]]]] = None,
                 target_prefix: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketLoggingV2Args.__new__(BucketLoggingV2Args)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            __props__.__dict__["expected_bucket_owner"] = expected_bucket_owner
            if target_bucket is None and not opts.urn:
                raise TypeError("Missing required property 'target_bucket'")
            __props__.__dict__["target_bucket"] = target_bucket
            __props__.__dict__["target_grants"] = target_grants
            if target_prefix is None and not opts.urn:
                raise TypeError("Missing required property 'target_prefix'")
            __props__.__dict__["target_prefix"] = target_prefix
        super(BucketLoggingV2, __self__).__init__(
            'aws:s3/bucketLoggingV2:BucketLoggingV2',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            expected_bucket_owner: Optional[pulumi.Input[str]] = None,
            target_bucket: Optional[pulumi.Input[str]] = None,
            target_grants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLoggingV2TargetGrantArgs']]]]] = None,
            target_prefix: Optional[pulumi.Input[str]] = None) -> 'BucketLoggingV2':
        """
        Get an existing BucketLoggingV2 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the bucket.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner.
        :param pulumi.Input[str] target_bucket: Name of the bucket where you want Amazon S3 to store server access logs.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLoggingV2TargetGrantArgs']]]] target_grants: Set of configuration blocks with information for granting permissions. See below.
        :param pulumi.Input[str] target_prefix: Prefix for all log object keys.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BucketLoggingV2State.__new__(_BucketLoggingV2State)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["expected_bucket_owner"] = expected_bucket_owner
        __props__.__dict__["target_bucket"] = target_bucket
        __props__.__dict__["target_grants"] = target_grants
        __props__.__dict__["target_prefix"] = target_prefix
        return BucketLoggingV2(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        Name of the bucket.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> pulumi.Output[Optional[str]]:
        """
        Account ID of the expected bucket owner.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @property
    @pulumi.getter(name="targetBucket")
    def target_bucket(self) -> pulumi.Output[str]:
        """
        Name of the bucket where you want Amazon S3 to store server access logs.
        """
        return pulumi.get(self, "target_bucket")

    @property
    @pulumi.getter(name="targetGrants")
    def target_grants(self) -> pulumi.Output[Optional[Sequence['outputs.BucketLoggingV2TargetGrant']]]:
        """
        Set of configuration blocks with information for granting permissions. See below.
        """
        return pulumi.get(self, "target_grants")

    @property
    @pulumi.getter(name="targetPrefix")
    def target_prefix(self) -> pulumi.Output[str]:
        """
        Prefix for all log object keys.
        """
        return pulumi.get(self, "target_prefix")

