# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['LbCertificateAttachmentArgs', 'LbCertificateAttachment']

@pulumi.input_type
class LbCertificateAttachmentArgs:
    def __init__(__self__, *,
                 certificate_name: pulumi.Input[str],
                 lb_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a LbCertificateAttachment resource.
        :param pulumi.Input[str] certificate_name: The name of your SSL/TLS certificate.
        :param pulumi.Input[str] lb_name: The name of the load balancer to which you want to associate the SSL/TLS certificate.
        """
        pulumi.set(__self__, "certificate_name", certificate_name)
        pulumi.set(__self__, "lb_name", lb_name)

    @property
    @pulumi.getter(name="certificateName")
    def certificate_name(self) -> pulumi.Input[str]:
        """
        The name of your SSL/TLS certificate.
        """
        return pulumi.get(self, "certificate_name")

    @certificate_name.setter
    def certificate_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate_name", value)

    @property
    @pulumi.getter(name="lbName")
    def lb_name(self) -> pulumi.Input[str]:
        """
        The name of the load balancer to which you want to associate the SSL/TLS certificate.
        """
        return pulumi.get(self, "lb_name")

    @lb_name.setter
    def lb_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "lb_name", value)


@pulumi.input_type
class _LbCertificateAttachmentState:
    def __init__(__self__, *,
                 certificate_name: Optional[pulumi.Input[str]] = None,
                 lb_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LbCertificateAttachment resources.
        :param pulumi.Input[str] certificate_name: The name of your SSL/TLS certificate.
        :param pulumi.Input[str] lb_name: The name of the load balancer to which you want to associate the SSL/TLS certificate.
        """
        if certificate_name is not None:
            pulumi.set(__self__, "certificate_name", certificate_name)
        if lb_name is not None:
            pulumi.set(__self__, "lb_name", lb_name)

    @property
    @pulumi.getter(name="certificateName")
    def certificate_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of your SSL/TLS certificate.
        """
        return pulumi.get(self, "certificate_name")

    @certificate_name.setter
    def certificate_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_name", value)

    @property
    @pulumi.getter(name="lbName")
    def lb_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the load balancer to which you want to associate the SSL/TLS certificate.
        """
        return pulumi.get(self, "lb_name")

    @lb_name.setter
    def lb_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lb_name", value)


class LbCertificateAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_name: Optional[pulumi.Input[str]] = None,
                 lb_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Attaches a Lightsail Load Balancer Certificate to a Lightsail Load Balancer.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test_lb = aws.lightsail.Lb("testLb",
            health_check_path="/",
            instance_port=80,
            tags={
                "foo": "bar",
            })
        test_lb_certificate = aws.lightsail.LbCertificate("testLbCertificate",
            lb_name=test_lb.id,
            domain_name="test.com")
        test_lb_certificate_attachment = aws.lightsail.LbCertificateAttachment("testLbCertificateAttachment",
            lb_name=test_lb.name,
            certificate_name=test_lb_certificate.name)
        ```

        ## Import

        `aws_lightsail_lb_certificate_attachment` can be imported by using the name attribute, e.g.,

        ```sh
         $ pulumi import aws:lightsail/lbCertificateAttachment:LbCertificateAttachment test example-load-balancer,example-certificate
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_name: The name of your SSL/TLS certificate.
        :param pulumi.Input[str] lb_name: The name of the load balancer to which you want to associate the SSL/TLS certificate.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LbCertificateAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attaches a Lightsail Load Balancer Certificate to a Lightsail Load Balancer.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test_lb = aws.lightsail.Lb("testLb",
            health_check_path="/",
            instance_port=80,
            tags={
                "foo": "bar",
            })
        test_lb_certificate = aws.lightsail.LbCertificate("testLbCertificate",
            lb_name=test_lb.id,
            domain_name="test.com")
        test_lb_certificate_attachment = aws.lightsail.LbCertificateAttachment("testLbCertificateAttachment",
            lb_name=test_lb.name,
            certificate_name=test_lb_certificate.name)
        ```

        ## Import

        `aws_lightsail_lb_certificate_attachment` can be imported by using the name attribute, e.g.,

        ```sh
         $ pulumi import aws:lightsail/lbCertificateAttachment:LbCertificateAttachment test example-load-balancer,example-certificate
        ```

        :param str resource_name: The name of the resource.
        :param LbCertificateAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LbCertificateAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_name: Optional[pulumi.Input[str]] = None,
                 lb_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LbCertificateAttachmentArgs.__new__(LbCertificateAttachmentArgs)

            if certificate_name is None and not opts.urn:
                raise TypeError("Missing required property 'certificate_name'")
            __props__.__dict__["certificate_name"] = certificate_name
            if lb_name is None and not opts.urn:
                raise TypeError("Missing required property 'lb_name'")
            __props__.__dict__["lb_name"] = lb_name
        super(LbCertificateAttachment, __self__).__init__(
            'aws:lightsail/lbCertificateAttachment:LbCertificateAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            certificate_name: Optional[pulumi.Input[str]] = None,
            lb_name: Optional[pulumi.Input[str]] = None) -> 'LbCertificateAttachment':
        """
        Get an existing LbCertificateAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_name: The name of your SSL/TLS certificate.
        :param pulumi.Input[str] lb_name: The name of the load balancer to which you want to associate the SSL/TLS certificate.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LbCertificateAttachmentState.__new__(_LbCertificateAttachmentState)

        __props__.__dict__["certificate_name"] = certificate_name
        __props__.__dict__["lb_name"] = lb_name
        return LbCertificateAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="certificateName")
    def certificate_name(self) -> pulumi.Output[str]:
        """
        The name of your SSL/TLS certificate.
        """
        return pulumi.get(self, "certificate_name")

    @property
    @pulumi.getter(name="lbName")
    def lb_name(self) -> pulumi.Output[str]:
        """
        The name of the load balancer to which you want to associate the SSL/TLS certificate.
        """
        return pulumi.get(self, "lb_name")

