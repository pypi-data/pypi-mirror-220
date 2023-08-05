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

__all__ = ['ImageRecipeArgs', 'ImageRecipe']

@pulumi.input_type
class ImageRecipeArgs:
    def __init__(__self__, *,
                 components: pulumi.Input[Sequence[pulumi.Input['ImageRecipeComponentArgs']]],
                 parent_image: pulumi.Input[str],
                 version: pulumi.Input[str],
                 block_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRecipeBlockDeviceMappingArgs']]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 systems_manager_agent: Optional[pulumi.Input['ImageRecipeSystemsManagerAgentArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_data_base64: Optional[pulumi.Input[str]] = None,
                 working_directory: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ImageRecipe resource.
        :param pulumi.Input[Sequence[pulumi.Input['ImageRecipeComponentArgs']]] components: Ordered configuration block(s) with components for the image recipe. Detailed below.
        :param pulumi.Input[str] parent_image: The image recipe uses this image as a base from which to build your customized image. The value can be the base image ARN or an AMI ID.
        :param pulumi.Input[str] version: The semantic version of the image recipe, which specifies the version in the following format, with numeric values in each position to indicate a specific version: major.minor.patch. For example: 1.0.0.
               
               The following attributes are optional:
        :param pulumi.Input[Sequence[pulumi.Input['ImageRecipeBlockDeviceMappingArgs']]] block_device_mappings: Configuration block(s) with block device mappings for the image recipe. Detailed below.
        :param pulumi.Input[str] description: Description of the image recipe.
        :param pulumi.Input[str] name: Name of the image recipe.
        :param pulumi.Input['ImageRecipeSystemsManagerAgentArgs'] systems_manager_agent: Configuration block for the Systems Manager Agent installed by default by Image Builder. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags for the image recipe. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] user_data_base64: Base64 encoded user data. Use this to provide commands or a command script to run when you launch your build instance.
        :param pulumi.Input[str] working_directory: The working directory to be used during build and test workflows.
        """
        pulumi.set(__self__, "components", components)
        pulumi.set(__self__, "parent_image", parent_image)
        pulumi.set(__self__, "version", version)
        if block_device_mappings is not None:
            pulumi.set(__self__, "block_device_mappings", block_device_mappings)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if systems_manager_agent is not None:
            pulumi.set(__self__, "systems_manager_agent", systems_manager_agent)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if user_data_base64 is not None:
            pulumi.set(__self__, "user_data_base64", user_data_base64)
        if working_directory is not None:
            pulumi.set(__self__, "working_directory", working_directory)

    @property
    @pulumi.getter
    def components(self) -> pulumi.Input[Sequence[pulumi.Input['ImageRecipeComponentArgs']]]:
        """
        Ordered configuration block(s) with components for the image recipe. Detailed below.
        """
        return pulumi.get(self, "components")

    @components.setter
    def components(self, value: pulumi.Input[Sequence[pulumi.Input['ImageRecipeComponentArgs']]]):
        pulumi.set(self, "components", value)

    @property
    @pulumi.getter(name="parentImage")
    def parent_image(self) -> pulumi.Input[str]:
        """
        The image recipe uses this image as a base from which to build your customized image. The value can be the base image ARN or an AMI ID.
        """
        return pulumi.get(self, "parent_image")

    @parent_image.setter
    def parent_image(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent_image", value)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[str]:
        """
        The semantic version of the image recipe, which specifies the version in the following format, with numeric values in each position to indicate a specific version: major.minor.patch. For example: 1.0.0.

        The following attributes are optional:
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: pulumi.Input[str]):
        pulumi.set(self, "version", value)

    @property
    @pulumi.getter(name="blockDeviceMappings")
    def block_device_mappings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ImageRecipeBlockDeviceMappingArgs']]]]:
        """
        Configuration block(s) with block device mappings for the image recipe. Detailed below.
        """
        return pulumi.get(self, "block_device_mappings")

    @block_device_mappings.setter
    def block_device_mappings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRecipeBlockDeviceMappingArgs']]]]):
        pulumi.set(self, "block_device_mappings", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the image recipe.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the image recipe.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="systemsManagerAgent")
    def systems_manager_agent(self) -> Optional[pulumi.Input['ImageRecipeSystemsManagerAgentArgs']]:
        """
        Configuration block for the Systems Manager Agent installed by default by Image Builder. Detailed below.
        """
        return pulumi.get(self, "systems_manager_agent")

    @systems_manager_agent.setter
    def systems_manager_agent(self, value: Optional[pulumi.Input['ImageRecipeSystemsManagerAgentArgs']]):
        pulumi.set(self, "systems_manager_agent", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags for the image recipe. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="userDataBase64")
    def user_data_base64(self) -> Optional[pulumi.Input[str]]:
        """
        Base64 encoded user data. Use this to provide commands or a command script to run when you launch your build instance.
        """
        return pulumi.get(self, "user_data_base64")

    @user_data_base64.setter
    def user_data_base64(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_data_base64", value)

    @property
    @pulumi.getter(name="workingDirectory")
    def working_directory(self) -> Optional[pulumi.Input[str]]:
        """
        The working directory to be used during build and test workflows.
        """
        return pulumi.get(self, "working_directory")

    @working_directory.setter
    def working_directory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "working_directory", value)


@pulumi.input_type
class _ImageRecipeState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 block_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRecipeBlockDeviceMappingArgs']]]] = None,
                 components: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRecipeComponentArgs']]]] = None,
                 date_created: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 parent_image: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[str]] = None,
                 systems_manager_agent: Optional[pulumi.Input['ImageRecipeSystemsManagerAgentArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_data_base64: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 working_directory: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ImageRecipe resources.
        :param pulumi.Input[str] arn: (Required) Amazon Resource Name (ARN) of the image recipe.
        :param pulumi.Input[Sequence[pulumi.Input['ImageRecipeBlockDeviceMappingArgs']]] block_device_mappings: Configuration block(s) with block device mappings for the image recipe. Detailed below.
        :param pulumi.Input[Sequence[pulumi.Input['ImageRecipeComponentArgs']]] components: Ordered configuration block(s) with components for the image recipe. Detailed below.
        :param pulumi.Input[str] date_created: Date the image recipe was created.
        :param pulumi.Input[str] description: Description of the image recipe.
        :param pulumi.Input[str] name: Name of the image recipe.
        :param pulumi.Input[str] owner: Owner of the image recipe.
        :param pulumi.Input[str] parent_image: The image recipe uses this image as a base from which to build your customized image. The value can be the base image ARN or an AMI ID.
        :param pulumi.Input[str] platform: Platform of the image recipe.
        :param pulumi.Input['ImageRecipeSystemsManagerAgentArgs'] systems_manager_agent: Configuration block for the Systems Manager Agent installed by default by Image Builder. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags for the image recipe. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] user_data_base64: Base64 encoded user data. Use this to provide commands or a command script to run when you launch your build instance.
        :param pulumi.Input[str] version: The semantic version of the image recipe, which specifies the version in the following format, with numeric values in each position to indicate a specific version: major.minor.patch. For example: 1.0.0.
               
               The following attributes are optional:
        :param pulumi.Input[str] working_directory: The working directory to be used during build and test workflows.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if block_device_mappings is not None:
            pulumi.set(__self__, "block_device_mappings", block_device_mappings)
        if components is not None:
            pulumi.set(__self__, "components", components)
        if date_created is not None:
            pulumi.set(__self__, "date_created", date_created)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if owner is not None:
            pulumi.set(__self__, "owner", owner)
        if parent_image is not None:
            pulumi.set(__self__, "parent_image", parent_image)
        if platform is not None:
            pulumi.set(__self__, "platform", platform)
        if systems_manager_agent is not None:
            pulumi.set(__self__, "systems_manager_agent", systems_manager_agent)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if user_data_base64 is not None:
            pulumi.set(__self__, "user_data_base64", user_data_base64)
        if version is not None:
            pulumi.set(__self__, "version", version)
        if working_directory is not None:
            pulumi.set(__self__, "working_directory", working_directory)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        (Required) Amazon Resource Name (ARN) of the image recipe.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="blockDeviceMappings")
    def block_device_mappings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ImageRecipeBlockDeviceMappingArgs']]]]:
        """
        Configuration block(s) with block device mappings for the image recipe. Detailed below.
        """
        return pulumi.get(self, "block_device_mappings")

    @block_device_mappings.setter
    def block_device_mappings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRecipeBlockDeviceMappingArgs']]]]):
        pulumi.set(self, "block_device_mappings", value)

    @property
    @pulumi.getter
    def components(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ImageRecipeComponentArgs']]]]:
        """
        Ordered configuration block(s) with components for the image recipe. Detailed below.
        """
        return pulumi.get(self, "components")

    @components.setter
    def components(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRecipeComponentArgs']]]]):
        pulumi.set(self, "components", value)

    @property
    @pulumi.getter(name="dateCreated")
    def date_created(self) -> Optional[pulumi.Input[str]]:
        """
        Date the image recipe was created.
        """
        return pulumi.get(self, "date_created")

    @date_created.setter
    def date_created(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "date_created", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the image recipe.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the image recipe.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def owner(self) -> Optional[pulumi.Input[str]]:
        """
        Owner of the image recipe.
        """
        return pulumi.get(self, "owner")

    @owner.setter
    def owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner", value)

    @property
    @pulumi.getter(name="parentImage")
    def parent_image(self) -> Optional[pulumi.Input[str]]:
        """
        The image recipe uses this image as a base from which to build your customized image. The value can be the base image ARN or an AMI ID.
        """
        return pulumi.get(self, "parent_image")

    @parent_image.setter
    def parent_image(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_image", value)

    @property
    @pulumi.getter
    def platform(self) -> Optional[pulumi.Input[str]]:
        """
        Platform of the image recipe.
        """
        return pulumi.get(self, "platform")

    @platform.setter
    def platform(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "platform", value)

    @property
    @pulumi.getter(name="systemsManagerAgent")
    def systems_manager_agent(self) -> Optional[pulumi.Input['ImageRecipeSystemsManagerAgentArgs']]:
        """
        Configuration block for the Systems Manager Agent installed by default by Image Builder. Detailed below.
        """
        return pulumi.get(self, "systems_manager_agent")

    @systems_manager_agent.setter
    def systems_manager_agent(self, value: Optional[pulumi.Input['ImageRecipeSystemsManagerAgentArgs']]):
        pulumi.set(self, "systems_manager_agent", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags for the image recipe. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="userDataBase64")
    def user_data_base64(self) -> Optional[pulumi.Input[str]]:
        """
        Base64 encoded user data. Use this to provide commands or a command script to run when you launch your build instance.
        """
        return pulumi.get(self, "user_data_base64")

    @user_data_base64.setter
    def user_data_base64(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_data_base64", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The semantic version of the image recipe, which specifies the version in the following format, with numeric values in each position to indicate a specific version: major.minor.patch. For example: 1.0.0.

        The following attributes are optional:
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)

    @property
    @pulumi.getter(name="workingDirectory")
    def working_directory(self) -> Optional[pulumi.Input[str]]:
        """
        The working directory to be used during build and test workflows.
        """
        return pulumi.get(self, "working_directory")

    @working_directory.setter
    def working_directory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "working_directory", value)


class ImageRecipe(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 block_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeBlockDeviceMappingArgs']]]]] = None,
                 components: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeComponentArgs']]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_image: Optional[pulumi.Input[str]] = None,
                 systems_manager_agent: Optional[pulumi.Input[pulumi.InputType['ImageRecipeSystemsManagerAgentArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_data_base64: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 working_directory: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an Image Builder Image Recipe.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.imagebuilder.ImageRecipe("example",
            block_device_mappings=[aws.imagebuilder.ImageRecipeBlockDeviceMappingArgs(
                device_name="/dev/xvdb",
                ebs=aws.imagebuilder.ImageRecipeBlockDeviceMappingEbsArgs(
                    delete_on_termination="true",
                    volume_size=100,
                    volume_type="gp2",
                ),
            )],
            components=[aws.imagebuilder.ImageRecipeComponentArgs(
                component_arn=aws_imagebuilder_component["example"]["arn"],
                parameters=[
                    aws.imagebuilder.ImageRecipeComponentParameterArgs(
                        name="Parameter1",
                        value="Value1",
                    ),
                    aws.imagebuilder.ImageRecipeComponentParameterArgs(
                        name="Parameter2",
                        value="Value2",
                    ),
                ],
            )],
            parent_image=f"arn:{data['aws_partition']['current']['partition']}:imagebuilder:{data['aws_region']['current']['name']}:aws:image/amazon-linux-2-x86/x.x.x",
            version="1.0.0")
        ```

        ## Import

        `aws_imagebuilder_image_recipe` resources can be imported by using the Amazon Resource Name (ARN), e.g.,

        ```sh
         $ pulumi import aws:imagebuilder/imageRecipe:ImageRecipe example arn:aws:imagebuilder:us-east-1:123456789012:image-recipe/example/1.0.0
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeBlockDeviceMappingArgs']]]] block_device_mappings: Configuration block(s) with block device mappings for the image recipe. Detailed below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeComponentArgs']]]] components: Ordered configuration block(s) with components for the image recipe. Detailed below.
        :param pulumi.Input[str] description: Description of the image recipe.
        :param pulumi.Input[str] name: Name of the image recipe.
        :param pulumi.Input[str] parent_image: The image recipe uses this image as a base from which to build your customized image. The value can be the base image ARN or an AMI ID.
        :param pulumi.Input[pulumi.InputType['ImageRecipeSystemsManagerAgentArgs']] systems_manager_agent: Configuration block for the Systems Manager Agent installed by default by Image Builder. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags for the image recipe. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] user_data_base64: Base64 encoded user data. Use this to provide commands or a command script to run when you launch your build instance.
        :param pulumi.Input[str] version: The semantic version of the image recipe, which specifies the version in the following format, with numeric values in each position to indicate a specific version: major.minor.patch. For example: 1.0.0.
               
               The following attributes are optional:
        :param pulumi.Input[str] working_directory: The working directory to be used during build and test workflows.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ImageRecipeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Image Builder Image Recipe.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.imagebuilder.ImageRecipe("example",
            block_device_mappings=[aws.imagebuilder.ImageRecipeBlockDeviceMappingArgs(
                device_name="/dev/xvdb",
                ebs=aws.imagebuilder.ImageRecipeBlockDeviceMappingEbsArgs(
                    delete_on_termination="true",
                    volume_size=100,
                    volume_type="gp2",
                ),
            )],
            components=[aws.imagebuilder.ImageRecipeComponentArgs(
                component_arn=aws_imagebuilder_component["example"]["arn"],
                parameters=[
                    aws.imagebuilder.ImageRecipeComponentParameterArgs(
                        name="Parameter1",
                        value="Value1",
                    ),
                    aws.imagebuilder.ImageRecipeComponentParameterArgs(
                        name="Parameter2",
                        value="Value2",
                    ),
                ],
            )],
            parent_image=f"arn:{data['aws_partition']['current']['partition']}:imagebuilder:{data['aws_region']['current']['name']}:aws:image/amazon-linux-2-x86/x.x.x",
            version="1.0.0")
        ```

        ## Import

        `aws_imagebuilder_image_recipe` resources can be imported by using the Amazon Resource Name (ARN), e.g.,

        ```sh
         $ pulumi import aws:imagebuilder/imageRecipe:ImageRecipe example arn:aws:imagebuilder:us-east-1:123456789012:image-recipe/example/1.0.0
        ```

        :param str resource_name: The name of the resource.
        :param ImageRecipeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ImageRecipeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 block_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeBlockDeviceMappingArgs']]]]] = None,
                 components: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeComponentArgs']]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_image: Optional[pulumi.Input[str]] = None,
                 systems_manager_agent: Optional[pulumi.Input[pulumi.InputType['ImageRecipeSystemsManagerAgentArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_data_base64: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 working_directory: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ImageRecipeArgs.__new__(ImageRecipeArgs)

            __props__.__dict__["block_device_mappings"] = block_device_mappings
            if components is None and not opts.urn:
                raise TypeError("Missing required property 'components'")
            __props__.__dict__["components"] = components
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            if parent_image is None and not opts.urn:
                raise TypeError("Missing required property 'parent_image'")
            __props__.__dict__["parent_image"] = parent_image
            __props__.__dict__["systems_manager_agent"] = systems_manager_agent
            __props__.__dict__["tags"] = tags
            __props__.__dict__["user_data_base64"] = user_data_base64
            if version is None and not opts.urn:
                raise TypeError("Missing required property 'version'")
            __props__.__dict__["version"] = version
            __props__.__dict__["working_directory"] = working_directory
            __props__.__dict__["arn"] = None
            __props__.__dict__["date_created"] = None
            __props__.__dict__["owner"] = None
            __props__.__dict__["platform"] = None
            __props__.__dict__["tags_all"] = None
        super(ImageRecipe, __self__).__init__(
            'aws:imagebuilder/imageRecipe:ImageRecipe',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            block_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeBlockDeviceMappingArgs']]]]] = None,
            components: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeComponentArgs']]]]] = None,
            date_created: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            owner: Optional[pulumi.Input[str]] = None,
            parent_image: Optional[pulumi.Input[str]] = None,
            platform: Optional[pulumi.Input[str]] = None,
            systems_manager_agent: Optional[pulumi.Input[pulumi.InputType['ImageRecipeSystemsManagerAgentArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            user_data_base64: Optional[pulumi.Input[str]] = None,
            version: Optional[pulumi.Input[str]] = None,
            working_directory: Optional[pulumi.Input[str]] = None) -> 'ImageRecipe':
        """
        Get an existing ImageRecipe resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: (Required) Amazon Resource Name (ARN) of the image recipe.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeBlockDeviceMappingArgs']]]] block_device_mappings: Configuration block(s) with block device mappings for the image recipe. Detailed below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRecipeComponentArgs']]]] components: Ordered configuration block(s) with components for the image recipe. Detailed below.
        :param pulumi.Input[str] date_created: Date the image recipe was created.
        :param pulumi.Input[str] description: Description of the image recipe.
        :param pulumi.Input[str] name: Name of the image recipe.
        :param pulumi.Input[str] owner: Owner of the image recipe.
        :param pulumi.Input[str] parent_image: The image recipe uses this image as a base from which to build your customized image. The value can be the base image ARN or an AMI ID.
        :param pulumi.Input[str] platform: Platform of the image recipe.
        :param pulumi.Input[pulumi.InputType['ImageRecipeSystemsManagerAgentArgs']] systems_manager_agent: Configuration block for the Systems Manager Agent installed by default by Image Builder. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags for the image recipe. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] user_data_base64: Base64 encoded user data. Use this to provide commands or a command script to run when you launch your build instance.
        :param pulumi.Input[str] version: The semantic version of the image recipe, which specifies the version in the following format, with numeric values in each position to indicate a specific version: major.minor.patch. For example: 1.0.0.
               
               The following attributes are optional:
        :param pulumi.Input[str] working_directory: The working directory to be used during build and test workflows.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ImageRecipeState.__new__(_ImageRecipeState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["block_device_mappings"] = block_device_mappings
        __props__.__dict__["components"] = components
        __props__.__dict__["date_created"] = date_created
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["owner"] = owner
        __props__.__dict__["parent_image"] = parent_image
        __props__.__dict__["platform"] = platform
        __props__.__dict__["systems_manager_agent"] = systems_manager_agent
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["user_data_base64"] = user_data_base64
        __props__.__dict__["version"] = version
        __props__.__dict__["working_directory"] = working_directory
        return ImageRecipe(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        (Required) Amazon Resource Name (ARN) of the image recipe.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="blockDeviceMappings")
    def block_device_mappings(self) -> pulumi.Output[Optional[Sequence['outputs.ImageRecipeBlockDeviceMapping']]]:
        """
        Configuration block(s) with block device mappings for the image recipe. Detailed below.
        """
        return pulumi.get(self, "block_device_mappings")

    @property
    @pulumi.getter
    def components(self) -> pulumi.Output[Sequence['outputs.ImageRecipeComponent']]:
        """
        Ordered configuration block(s) with components for the image recipe. Detailed below.
        """
        return pulumi.get(self, "components")

    @property
    @pulumi.getter(name="dateCreated")
    def date_created(self) -> pulumi.Output[str]:
        """
        Date the image recipe was created.
        """
        return pulumi.get(self, "date_created")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the image recipe.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the image recipe.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def owner(self) -> pulumi.Output[str]:
        """
        Owner of the image recipe.
        """
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter(name="parentImage")
    def parent_image(self) -> pulumi.Output[str]:
        """
        The image recipe uses this image as a base from which to build your customized image. The value can be the base image ARN or an AMI ID.
        """
        return pulumi.get(self, "parent_image")

    @property
    @pulumi.getter
    def platform(self) -> pulumi.Output[str]:
        """
        Platform of the image recipe.
        """
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter(name="systemsManagerAgent")
    def systems_manager_agent(self) -> pulumi.Output['outputs.ImageRecipeSystemsManagerAgent']:
        """
        Configuration block for the Systems Manager Agent installed by default by Image Builder. Detailed below.
        """
        return pulumi.get(self, "systems_manager_agent")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags for the image recipe. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="userDataBase64")
    def user_data_base64(self) -> pulumi.Output[str]:
        """
        Base64 encoded user data. Use this to provide commands or a command script to run when you launch your build instance.
        """
        return pulumi.get(self, "user_data_base64")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        The semantic version of the image recipe, which specifies the version in the following format, with numeric values in each position to indicate a specific version: major.minor.patch. For example: 1.0.0.

        The following attributes are optional:
        """
        return pulumi.get(self, "version")

    @property
    @pulumi.getter(name="workingDirectory")
    def working_directory(self) -> pulumi.Output[Optional[str]]:
        """
        The working directory to be used during build and test workflows.
        """
        return pulumi.get(self, "working_directory")

