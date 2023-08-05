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

__all__ = ['LoadBalancerPolicyArgs', 'LoadBalancerPolicy']

@pulumi.input_type
class LoadBalancerPolicyArgs:
    def __init__(__self__, *,
                 load_balancer_name: pulumi.Input[str],
                 policy_name: pulumi.Input[str],
                 policy_type_name: pulumi.Input[str],
                 policy_attributes: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerPolicyPolicyAttributeArgs']]]] = None):
        """
        The set of arguments for constructing a LoadBalancerPolicy resource.
        :param pulumi.Input[str] load_balancer_name: The load balancer on which the policy is defined.
        :param pulumi.Input[str] policy_name: The name of the load balancer policy.
        :param pulumi.Input[str] policy_type_name: The policy type.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancerPolicyPolicyAttributeArgs']]] policy_attributes: Policy attribute to apply to the policy.
        """
        pulumi.set(__self__, "load_balancer_name", load_balancer_name)
        pulumi.set(__self__, "policy_name", policy_name)
        pulumi.set(__self__, "policy_type_name", policy_type_name)
        if policy_attributes is not None:
            pulumi.set(__self__, "policy_attributes", policy_attributes)

    @property
    @pulumi.getter(name="loadBalancerName")
    def load_balancer_name(self) -> pulumi.Input[str]:
        """
        The load balancer on which the policy is defined.
        """
        return pulumi.get(self, "load_balancer_name")

    @load_balancer_name.setter
    def load_balancer_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "load_balancer_name", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Input[str]:
        """
        The name of the load balancer policy.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter(name="policyTypeName")
    def policy_type_name(self) -> pulumi.Input[str]:
        """
        The policy type.
        """
        return pulumi.get(self, "policy_type_name")

    @policy_type_name.setter
    def policy_type_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_type_name", value)

    @property
    @pulumi.getter(name="policyAttributes")
    def policy_attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerPolicyPolicyAttributeArgs']]]]:
        """
        Policy attribute to apply to the policy.
        """
        return pulumi.get(self, "policy_attributes")

    @policy_attributes.setter
    def policy_attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerPolicyPolicyAttributeArgs']]]]):
        pulumi.set(self, "policy_attributes", value)


@pulumi.input_type
class _LoadBalancerPolicyState:
    def __init__(__self__, *,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 policy_attributes: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerPolicyPolicyAttributeArgs']]]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 policy_type_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LoadBalancerPolicy resources.
        :param pulumi.Input[str] load_balancer_name: The load balancer on which the policy is defined.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancerPolicyPolicyAttributeArgs']]] policy_attributes: Policy attribute to apply to the policy.
        :param pulumi.Input[str] policy_name: The name of the load balancer policy.
        :param pulumi.Input[str] policy_type_name: The policy type.
        """
        if load_balancer_name is not None:
            pulumi.set(__self__, "load_balancer_name", load_balancer_name)
        if policy_attributes is not None:
            pulumi.set(__self__, "policy_attributes", policy_attributes)
        if policy_name is not None:
            pulumi.set(__self__, "policy_name", policy_name)
        if policy_type_name is not None:
            pulumi.set(__self__, "policy_type_name", policy_type_name)

    @property
    @pulumi.getter(name="loadBalancerName")
    def load_balancer_name(self) -> Optional[pulumi.Input[str]]:
        """
        The load balancer on which the policy is defined.
        """
        return pulumi.get(self, "load_balancer_name")

    @load_balancer_name.setter
    def load_balancer_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "load_balancer_name", value)

    @property
    @pulumi.getter(name="policyAttributes")
    def policy_attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerPolicyPolicyAttributeArgs']]]]:
        """
        Policy attribute to apply to the policy.
        """
        return pulumi.get(self, "policy_attributes")

    @policy_attributes.setter
    def policy_attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerPolicyPolicyAttributeArgs']]]]):
        pulumi.set(self, "policy_attributes", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the load balancer policy.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter(name="policyTypeName")
    def policy_type_name(self) -> Optional[pulumi.Input[str]]:
        """
        The policy type.
        """
        return pulumi.get(self, "policy_type_name")

    @policy_type_name.setter
    def policy_type_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_type_name", value)


warnings.warn("""aws.elasticloadbalancing.LoadBalancerPolicy has been deprecated in favor of aws.elb.LoadBalancerPolicy""", DeprecationWarning)


class LoadBalancerPolicy(pulumi.CustomResource):
    warnings.warn("""aws.elasticloadbalancing.LoadBalancerPolicy has been deprecated in favor of aws.elb.LoadBalancerPolicy""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 policy_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerPolicyPolicyAttributeArgs']]]]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 policy_type_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a load balancer policy, which can be attached to an ELB listener or backend server.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        wu_tang = aws.elb.LoadBalancer("wu-tang",
            availability_zones=["us-east-1a"],
            listeners=[aws.elb.LoadBalancerListenerArgs(
                instance_port=443,
                instance_protocol="http",
                lb_port=443,
                lb_protocol="https",
                ssl_certificate_id="arn:aws:iam::000000000000:server-certificate/wu-tang.net",
            )],
            tags={
                "Name": "wu-tang",
            })
        wu_tang_ca_pubkey_policy = aws.elb.LoadBalancerPolicy("wu-tang-ca-pubkey-policy",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ca-pubkey-policy",
            policy_type_name="PublicKeyPolicyType",
            policy_attributes=[aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                name="PublicKey",
                value=(lambda path: open(path).read())("wu-tang-pubkey"),
            )])
        wu_tang_root_ca_backend_auth_policy = aws.elb.LoadBalancerPolicy("wu-tang-root-ca-backend-auth-policy",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-root-ca-backend-auth-policy",
            policy_type_name="BackendServerAuthenticationPolicyType",
            policy_attributes=[aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                name="PublicKeyPolicyName",
                value=aws_load_balancer_policy["wu-tang-root-ca-pubkey-policy"]["policy_name"],
            )])
        wu_tang_ssl = aws.elb.LoadBalancerPolicy("wu-tang-ssl",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ssl",
            policy_type_name="SSLNegotiationPolicyType",
            policy_attributes=[
                aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                    name="ECDHE-ECDSA-AES128-GCM-SHA256",
                    value="true",
                ),
                aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                    name="Protocol-TLSv1.2",
                    value="true",
                ),
            ])
        wu_tang_ssl_tls_1_1 = aws.elb.LoadBalancerPolicy("wu-tang-ssl-tls-1-1",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ssl",
            policy_type_name="SSLNegotiationPolicyType",
            policy_attributes=[aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                name="Reference-Security-Policy",
                value="ELBSecurityPolicy-TLS-1-1-2017-01",
            )])
        wu_tang_backend_auth_policies_443 = aws.elb.LoadBalancerBackendServerPolicy("wu-tang-backend-auth-policies-443",
            load_balancer_name=wu_tang.name,
            instance_port=443,
            policy_names=[wu_tang_root_ca_backend_auth_policy.policy_name])
        wu_tang_listener_policies_443 = aws.elb.ListenerPolicy("wu-tang-listener-policies-443",
            load_balancer_name=wu_tang.name,
            load_balancer_port=443,
            policy_names=[wu_tang_ssl.policy_name])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] load_balancer_name: The load balancer on which the policy is defined.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerPolicyPolicyAttributeArgs']]]] policy_attributes: Policy attribute to apply to the policy.
        :param pulumi.Input[str] policy_name: The name of the load balancer policy.
        :param pulumi.Input[str] policy_type_name: The policy type.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LoadBalancerPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a load balancer policy, which can be attached to an ELB listener or backend server.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        wu_tang = aws.elb.LoadBalancer("wu-tang",
            availability_zones=["us-east-1a"],
            listeners=[aws.elb.LoadBalancerListenerArgs(
                instance_port=443,
                instance_protocol="http",
                lb_port=443,
                lb_protocol="https",
                ssl_certificate_id="arn:aws:iam::000000000000:server-certificate/wu-tang.net",
            )],
            tags={
                "Name": "wu-tang",
            })
        wu_tang_ca_pubkey_policy = aws.elb.LoadBalancerPolicy("wu-tang-ca-pubkey-policy",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ca-pubkey-policy",
            policy_type_name="PublicKeyPolicyType",
            policy_attributes=[aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                name="PublicKey",
                value=(lambda path: open(path).read())("wu-tang-pubkey"),
            )])
        wu_tang_root_ca_backend_auth_policy = aws.elb.LoadBalancerPolicy("wu-tang-root-ca-backend-auth-policy",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-root-ca-backend-auth-policy",
            policy_type_name="BackendServerAuthenticationPolicyType",
            policy_attributes=[aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                name="PublicKeyPolicyName",
                value=aws_load_balancer_policy["wu-tang-root-ca-pubkey-policy"]["policy_name"],
            )])
        wu_tang_ssl = aws.elb.LoadBalancerPolicy("wu-tang-ssl",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ssl",
            policy_type_name="SSLNegotiationPolicyType",
            policy_attributes=[
                aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                    name="ECDHE-ECDSA-AES128-GCM-SHA256",
                    value="true",
                ),
                aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                    name="Protocol-TLSv1.2",
                    value="true",
                ),
            ])
        wu_tang_ssl_tls_1_1 = aws.elb.LoadBalancerPolicy("wu-tang-ssl-tls-1-1",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ssl",
            policy_type_name="SSLNegotiationPolicyType",
            policy_attributes=[aws.elb.LoadBalancerPolicyPolicyAttributeArgs(
                name="Reference-Security-Policy",
                value="ELBSecurityPolicy-TLS-1-1-2017-01",
            )])
        wu_tang_backend_auth_policies_443 = aws.elb.LoadBalancerBackendServerPolicy("wu-tang-backend-auth-policies-443",
            load_balancer_name=wu_tang.name,
            instance_port=443,
            policy_names=[wu_tang_root_ca_backend_auth_policy.policy_name])
        wu_tang_listener_policies_443 = aws.elb.ListenerPolicy("wu-tang-listener-policies-443",
            load_balancer_name=wu_tang.name,
            load_balancer_port=443,
            policy_names=[wu_tang_ssl.policy_name])
        ```

        :param str resource_name: The name of the resource.
        :param LoadBalancerPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LoadBalancerPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 policy_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerPolicyPolicyAttributeArgs']]]]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 policy_type_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""LoadBalancerPolicy is deprecated: aws.elasticloadbalancing.LoadBalancerPolicy has been deprecated in favor of aws.elb.LoadBalancerPolicy""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LoadBalancerPolicyArgs.__new__(LoadBalancerPolicyArgs)

            if load_balancer_name is None and not opts.urn:
                raise TypeError("Missing required property 'load_balancer_name'")
            __props__.__dict__["load_balancer_name"] = load_balancer_name
            __props__.__dict__["policy_attributes"] = policy_attributes
            if policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'policy_name'")
            __props__.__dict__["policy_name"] = policy_name
            if policy_type_name is None and not opts.urn:
                raise TypeError("Missing required property 'policy_type_name'")
            __props__.__dict__["policy_type_name"] = policy_type_name
        super(LoadBalancerPolicy, __self__).__init__(
            'aws:elasticloadbalancing/loadBalancerPolicy:LoadBalancerPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            load_balancer_name: Optional[pulumi.Input[str]] = None,
            policy_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerPolicyPolicyAttributeArgs']]]]] = None,
            policy_name: Optional[pulumi.Input[str]] = None,
            policy_type_name: Optional[pulumi.Input[str]] = None) -> 'LoadBalancerPolicy':
        """
        Get an existing LoadBalancerPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] load_balancer_name: The load balancer on which the policy is defined.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerPolicyPolicyAttributeArgs']]]] policy_attributes: Policy attribute to apply to the policy.
        :param pulumi.Input[str] policy_name: The name of the load balancer policy.
        :param pulumi.Input[str] policy_type_name: The policy type.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LoadBalancerPolicyState.__new__(_LoadBalancerPolicyState)

        __props__.__dict__["load_balancer_name"] = load_balancer_name
        __props__.__dict__["policy_attributes"] = policy_attributes
        __props__.__dict__["policy_name"] = policy_name
        __props__.__dict__["policy_type_name"] = policy_type_name
        return LoadBalancerPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="loadBalancerName")
    def load_balancer_name(self) -> pulumi.Output[str]:
        """
        The load balancer on which the policy is defined.
        """
        return pulumi.get(self, "load_balancer_name")

    @property
    @pulumi.getter(name="policyAttributes")
    def policy_attributes(self) -> pulumi.Output[Sequence['outputs.LoadBalancerPolicyPolicyAttribute']]:
        """
        Policy attribute to apply to the policy.
        """
        return pulumi.get(self, "policy_attributes")

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Output[str]:
        """
        The name of the load balancer policy.
        """
        return pulumi.get(self, "policy_name")

    @property
    @pulumi.getter(name="policyTypeName")
    def policy_type_name(self) -> pulumi.Output[str]:
        """
        The policy type.
        """
        return pulumi.get(self, "policy_type_name")

