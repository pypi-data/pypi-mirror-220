# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['InvocationArgs', 'Invocation']

@pulumi.input_type
class InvocationArgs:
    def __init__(__self__, *,
                 function_name: pulumi.Input[str],
                 input: pulumi.Input[str],
                 qualifier: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Invocation resource.
        :param pulumi.Input[str] function_name: Name of the lambda function.
        :param pulumi.Input[str] input: JSON payload to the lambda function.
               
               The following arguments are optional:
        :param pulumi.Input[str] qualifier: Qualifier (i.e., version) of the lambda function. Defaults to `$LATEST`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger a re-invocation.
        """
        pulumi.set(__self__, "function_name", function_name)
        pulumi.set(__self__, "input", input)
        if qualifier is not None:
            pulumi.set(__self__, "qualifier", qualifier)
        if triggers is not None:
            pulumi.set(__self__, "triggers", triggers)

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> pulumi.Input[str]:
        """
        Name of the lambda function.
        """
        return pulumi.get(self, "function_name")

    @function_name.setter
    def function_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "function_name", value)

    @property
    @pulumi.getter
    def input(self) -> pulumi.Input[str]:
        """
        JSON payload to the lambda function.

        The following arguments are optional:
        """
        return pulumi.get(self, "input")

    @input.setter
    def input(self, value: pulumi.Input[str]):
        pulumi.set(self, "input", value)

    @property
    @pulumi.getter
    def qualifier(self) -> Optional[pulumi.Input[str]]:
        """
        Qualifier (i.e., version) of the lambda function. Defaults to `$LATEST`.
        """
        return pulumi.get(self, "qualifier")

    @qualifier.setter
    def qualifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "qualifier", value)

    @property
    @pulumi.getter
    def triggers(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of arbitrary keys and values that, when changed, will trigger a re-invocation.
        """
        return pulumi.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "triggers", value)


@pulumi.input_type
class _InvocationState:
    def __init__(__self__, *,
                 function_name: Optional[pulumi.Input[str]] = None,
                 input: Optional[pulumi.Input[str]] = None,
                 qualifier: Optional[pulumi.Input[str]] = None,
                 result: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Invocation resources.
        :param pulumi.Input[str] function_name: Name of the lambda function.
        :param pulumi.Input[str] input: JSON payload to the lambda function.
               
               The following arguments are optional:
        :param pulumi.Input[str] qualifier: Qualifier (i.e., version) of the lambda function. Defaults to `$LATEST`.
        :param pulumi.Input[str] result: String result of the lambda function invocation.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger a re-invocation.
        """
        if function_name is not None:
            pulumi.set(__self__, "function_name", function_name)
        if input is not None:
            pulumi.set(__self__, "input", input)
        if qualifier is not None:
            pulumi.set(__self__, "qualifier", qualifier)
        if result is not None:
            pulumi.set(__self__, "result", result)
        if triggers is not None:
            pulumi.set(__self__, "triggers", triggers)

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the lambda function.
        """
        return pulumi.get(self, "function_name")

    @function_name.setter
    def function_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "function_name", value)

    @property
    @pulumi.getter
    def input(self) -> Optional[pulumi.Input[str]]:
        """
        JSON payload to the lambda function.

        The following arguments are optional:
        """
        return pulumi.get(self, "input")

    @input.setter
    def input(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "input", value)

    @property
    @pulumi.getter
    def qualifier(self) -> Optional[pulumi.Input[str]]:
        """
        Qualifier (i.e., version) of the lambda function. Defaults to `$LATEST`.
        """
        return pulumi.get(self, "qualifier")

    @qualifier.setter
    def qualifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "qualifier", value)

    @property
    @pulumi.getter
    def result(self) -> Optional[pulumi.Input[str]]:
        """
        String result of the lambda function invocation.
        """
        return pulumi.get(self, "result")

    @result.setter
    def result(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "result", value)

    @property
    @pulumi.getter
    def triggers(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of arbitrary keys and values that, when changed, will trigger a re-invocation.
        """
        return pulumi.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "triggers", value)


class Invocation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 function_name: Optional[pulumi.Input[str]] = None,
                 input: Optional[pulumi.Input[str]] = None,
                 qualifier: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Use this resource to invoke a lambda function. The lambda function is invoked with the [RequestResponse](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_RequestSyntax) invocation type.

        > **NOTE:** This resource _only_ invokes the function when the arguments call for a create or update. In other words, after an initial invocation on _apply_, if the arguments do not change, a subsequent _apply_ does not invoke the function again. To dynamically invoke the function, see the `triggers` example below. To always invoke a function on each _apply_, see the `lambda.Invocation` data source.

        > **NOTE:** If you get a `KMSAccessDeniedException: Lambda was unable to decrypt the environment variables because KMS access was denied` error when invoking an `lambda.Function` with environment variables, the IAM role associated with the function may have been deleted and recreated _after_ the function was created. You can fix the problem two ways: 1) updating the function's role to another role and then updating it back again to the recreated role, or 2) by using Pulumi to `taint` the function and `apply` your configuration again to recreate the function. (When you create a function, Lambda grants permissions on the KMS key to the function's IAM role. If the IAM role is recreated, the grant is no longer valid. Changing the function's role or recreating the function causes Lambda to update the grant.)

        ## Example Usage
        ### Dynamic Invocation Example Using Triggers

        ```python
        import pulumi
        import hashlib
        import json
        import pulumi_aws as aws

        example = aws.lambda_.Invocation("example",
            function_name=aws_lambda_function["lambda_function_test"]["function_name"],
            triggers={
                "redeployment": hashlib.sha1(json.dumps([aws_lambda_function["example"]["environment"]]).encode()).hexdigest(),
            },
            input=json.dumps({
                "key1": "value1",
                "key2": "value2",
            }))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] function_name: Name of the lambda function.
        :param pulumi.Input[str] input: JSON payload to the lambda function.
               
               The following arguments are optional:
        :param pulumi.Input[str] qualifier: Qualifier (i.e., version) of the lambda function. Defaults to `$LATEST`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger a re-invocation.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InvocationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Use this resource to invoke a lambda function. The lambda function is invoked with the [RequestResponse](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_RequestSyntax) invocation type.

        > **NOTE:** This resource _only_ invokes the function when the arguments call for a create or update. In other words, after an initial invocation on _apply_, if the arguments do not change, a subsequent _apply_ does not invoke the function again. To dynamically invoke the function, see the `triggers` example below. To always invoke a function on each _apply_, see the `lambda.Invocation` data source.

        > **NOTE:** If you get a `KMSAccessDeniedException: Lambda was unable to decrypt the environment variables because KMS access was denied` error when invoking an `lambda.Function` with environment variables, the IAM role associated with the function may have been deleted and recreated _after_ the function was created. You can fix the problem two ways: 1) updating the function's role to another role and then updating it back again to the recreated role, or 2) by using Pulumi to `taint` the function and `apply` your configuration again to recreate the function. (When you create a function, Lambda grants permissions on the KMS key to the function's IAM role. If the IAM role is recreated, the grant is no longer valid. Changing the function's role or recreating the function causes Lambda to update the grant.)

        ## Example Usage
        ### Dynamic Invocation Example Using Triggers

        ```python
        import pulumi
        import hashlib
        import json
        import pulumi_aws as aws

        example = aws.lambda_.Invocation("example",
            function_name=aws_lambda_function["lambda_function_test"]["function_name"],
            triggers={
                "redeployment": hashlib.sha1(json.dumps([aws_lambda_function["example"]["environment"]]).encode()).hexdigest(),
            },
            input=json.dumps({
                "key1": "value1",
                "key2": "value2",
            }))
        ```

        :param str resource_name: The name of the resource.
        :param InvocationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InvocationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 function_name: Optional[pulumi.Input[str]] = None,
                 input: Optional[pulumi.Input[str]] = None,
                 qualifier: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InvocationArgs.__new__(InvocationArgs)

            if function_name is None and not opts.urn:
                raise TypeError("Missing required property 'function_name'")
            __props__.__dict__["function_name"] = function_name
            if input is None and not opts.urn:
                raise TypeError("Missing required property 'input'")
            __props__.__dict__["input"] = input
            __props__.__dict__["qualifier"] = qualifier
            __props__.__dict__["triggers"] = triggers
            __props__.__dict__["result"] = None
        super(Invocation, __self__).__init__(
            'aws:lambda/invocation:Invocation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            function_name: Optional[pulumi.Input[str]] = None,
            input: Optional[pulumi.Input[str]] = None,
            qualifier: Optional[pulumi.Input[str]] = None,
            result: Optional[pulumi.Input[str]] = None,
            triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Invocation':
        """
        Get an existing Invocation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] function_name: Name of the lambda function.
        :param pulumi.Input[str] input: JSON payload to the lambda function.
               
               The following arguments are optional:
        :param pulumi.Input[str] qualifier: Qualifier (i.e., version) of the lambda function. Defaults to `$LATEST`.
        :param pulumi.Input[str] result: String result of the lambda function invocation.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger a re-invocation.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InvocationState.__new__(_InvocationState)

        __props__.__dict__["function_name"] = function_name
        __props__.__dict__["input"] = input
        __props__.__dict__["qualifier"] = qualifier
        __props__.__dict__["result"] = result
        __props__.__dict__["triggers"] = triggers
        return Invocation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> pulumi.Output[str]:
        """
        Name of the lambda function.
        """
        return pulumi.get(self, "function_name")

    @property
    @pulumi.getter
    def input(self) -> pulumi.Output[str]:
        """
        JSON payload to the lambda function.

        The following arguments are optional:
        """
        return pulumi.get(self, "input")

    @property
    @pulumi.getter
    def qualifier(self) -> pulumi.Output[Optional[str]]:
        """
        Qualifier (i.e., version) of the lambda function. Defaults to `$LATEST`.
        """
        return pulumi.get(self, "qualifier")

    @property
    @pulumi.getter
    def result(self) -> pulumi.Output[str]:
        """
        String result of the lambda function invocation.
        """
        return pulumi.get(self, "result")

    @property
    @pulumi.getter
    def triggers(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of arbitrary keys and values that, when changed, will trigger a re-invocation.
        """
        return pulumi.get(self, "triggers")

