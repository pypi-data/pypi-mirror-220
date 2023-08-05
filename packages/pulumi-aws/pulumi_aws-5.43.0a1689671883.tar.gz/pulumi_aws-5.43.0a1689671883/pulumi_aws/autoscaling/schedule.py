# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ScheduleArgs', 'Schedule']

@pulumi.input_type
class ScheduleArgs:
    def __init__(__self__, *,
                 autoscaling_group_name: pulumi.Input[str],
                 scheduled_action_name: pulumi.Input[str],
                 desired_capacity: Optional[pulumi.Input[int]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 max_size: Optional[pulumi.Input[int]] = None,
                 min_size: Optional[pulumi.Input[int]] = None,
                 recurrence: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Schedule resource.
        :param pulumi.Input[str] autoscaling_group_name: The name of the Auto Scaling group.
        :param pulumi.Input[str] scheduled_action_name: The name of this scaling action.
               
               The following arguments are optional:
        :param pulumi.Input[int] desired_capacity: The initial capacity of the Auto Scaling group after the scheduled action runs and the capacity it attempts to maintain. Set to `-1` if you don't want to change the desired capacity at the scheduled time. Defaults to `0`.
        :param pulumi.Input[str] end_time: The date and time for the recurring schedule to end, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        :param pulumi.Input[int] max_size: The maximum size of the Auto Scaling group. Set to `-1` if you don't want to change the maximum size at the scheduled time. Defaults to `0`.
        :param pulumi.Input[int] min_size: The minimum size of the Auto Scaling group. Set to `-1` if you don't want to change the minimum size at the scheduled time. Defaults to `0`.
        :param pulumi.Input[str] recurrence: The recurring schedule for this action specified using the Unix cron syntax format.
        :param pulumi.Input[str] start_time: The date and time for the recurring schedule to start, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        :param pulumi.Input[str] time_zone: Specifies the time zone for a cron expression. Valid values are the canonical names of the IANA time zones (such as `Etc/GMT+9` or `Pacific/Tahiti`).
               
               > **NOTE:** When `start_time` and `end_time` are specified with `recurrence` , they form the boundaries of when the recurring action will start and stop.
        """
        pulumi.set(__self__, "autoscaling_group_name", autoscaling_group_name)
        pulumi.set(__self__, "scheduled_action_name", scheduled_action_name)
        if desired_capacity is not None:
            pulumi.set(__self__, "desired_capacity", desired_capacity)
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if max_size is not None:
            pulumi.set(__self__, "max_size", max_size)
        if min_size is not None:
            pulumi.set(__self__, "min_size", min_size)
        if recurrence is not None:
            pulumi.set(__self__, "recurrence", recurrence)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)
        if time_zone is not None:
            pulumi.set(__self__, "time_zone", time_zone)

    @property
    @pulumi.getter(name="autoscalingGroupName")
    def autoscaling_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Auto Scaling group.
        """
        return pulumi.get(self, "autoscaling_group_name")

    @autoscaling_group_name.setter
    def autoscaling_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "autoscaling_group_name", value)

    @property
    @pulumi.getter(name="scheduledActionName")
    def scheduled_action_name(self) -> pulumi.Input[str]:
        """
        The name of this scaling action.

        The following arguments are optional:
        """
        return pulumi.get(self, "scheduled_action_name")

    @scheduled_action_name.setter
    def scheduled_action_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "scheduled_action_name", value)

    @property
    @pulumi.getter(name="desiredCapacity")
    def desired_capacity(self) -> Optional[pulumi.Input[int]]:
        """
        The initial capacity of the Auto Scaling group after the scheduled action runs and the capacity it attempts to maintain. Set to `-1` if you don't want to change the desired capacity at the scheduled time. Defaults to `0`.
        """
        return pulumi.get(self, "desired_capacity")

    @desired_capacity.setter
    def desired_capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "desired_capacity", value)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time for the recurring schedule to end, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        """
        return pulumi.get(self, "end_time")

    @end_time.setter
    def end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_time", value)

    @property
    @pulumi.getter(name="maxSize")
    def max_size(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum size of the Auto Scaling group. Set to `-1` if you don't want to change the maximum size at the scheduled time. Defaults to `0`.
        """
        return pulumi.get(self, "max_size")

    @max_size.setter
    def max_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_size", value)

    @property
    @pulumi.getter(name="minSize")
    def min_size(self) -> Optional[pulumi.Input[int]]:
        """
        The minimum size of the Auto Scaling group. Set to `-1` if you don't want to change the minimum size at the scheduled time. Defaults to `0`.
        """
        return pulumi.get(self, "min_size")

    @min_size.setter
    def min_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_size", value)

    @property
    @pulumi.getter
    def recurrence(self) -> Optional[pulumi.Input[str]]:
        """
        The recurring schedule for this action specified using the Unix cron syntax format.
        """
        return pulumi.get(self, "recurrence")

    @recurrence.setter
    def recurrence(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "recurrence", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time for the recurring schedule to start, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_time", value)

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the time zone for a cron expression. Valid values are the canonical names of the IANA time zones (such as `Etc/GMT+9` or `Pacific/Tahiti`).

        > **NOTE:** When `start_time` and `end_time` are specified with `recurrence` , they form the boundaries of when the recurring action will start and stop.
        """
        return pulumi.get(self, "time_zone")

    @time_zone.setter
    def time_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "time_zone", value)


@pulumi.input_type
class _ScheduleState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 autoscaling_group_name: Optional[pulumi.Input[str]] = None,
                 desired_capacity: Optional[pulumi.Input[int]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 max_size: Optional[pulumi.Input[int]] = None,
                 min_size: Optional[pulumi.Input[int]] = None,
                 recurrence: Optional[pulumi.Input[str]] = None,
                 scheduled_action_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Schedule resources.
        :param pulumi.Input[str] arn: ARN assigned by AWS to the autoscaling schedule.
        :param pulumi.Input[str] autoscaling_group_name: The name of the Auto Scaling group.
        :param pulumi.Input[int] desired_capacity: The initial capacity of the Auto Scaling group after the scheduled action runs and the capacity it attempts to maintain. Set to `-1` if you don't want to change the desired capacity at the scheduled time. Defaults to `0`.
        :param pulumi.Input[str] end_time: The date and time for the recurring schedule to end, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        :param pulumi.Input[int] max_size: The maximum size of the Auto Scaling group. Set to `-1` if you don't want to change the maximum size at the scheduled time. Defaults to `0`.
        :param pulumi.Input[int] min_size: The minimum size of the Auto Scaling group. Set to `-1` if you don't want to change the minimum size at the scheduled time. Defaults to `0`.
        :param pulumi.Input[str] recurrence: The recurring schedule for this action specified using the Unix cron syntax format.
        :param pulumi.Input[str] scheduled_action_name: The name of this scaling action.
               
               The following arguments are optional:
        :param pulumi.Input[str] start_time: The date and time for the recurring schedule to start, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        :param pulumi.Input[str] time_zone: Specifies the time zone for a cron expression. Valid values are the canonical names of the IANA time zones (such as `Etc/GMT+9` or `Pacific/Tahiti`).
               
               > **NOTE:** When `start_time` and `end_time` are specified with `recurrence` , they form the boundaries of when the recurring action will start and stop.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if autoscaling_group_name is not None:
            pulumi.set(__self__, "autoscaling_group_name", autoscaling_group_name)
        if desired_capacity is not None:
            pulumi.set(__self__, "desired_capacity", desired_capacity)
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if max_size is not None:
            pulumi.set(__self__, "max_size", max_size)
        if min_size is not None:
            pulumi.set(__self__, "min_size", min_size)
        if recurrence is not None:
            pulumi.set(__self__, "recurrence", recurrence)
        if scheduled_action_name is not None:
            pulumi.set(__self__, "scheduled_action_name", scheduled_action_name)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)
        if time_zone is not None:
            pulumi.set(__self__, "time_zone", time_zone)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN assigned by AWS to the autoscaling schedule.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="autoscalingGroupName")
    def autoscaling_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Auto Scaling group.
        """
        return pulumi.get(self, "autoscaling_group_name")

    @autoscaling_group_name.setter
    def autoscaling_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "autoscaling_group_name", value)

    @property
    @pulumi.getter(name="desiredCapacity")
    def desired_capacity(self) -> Optional[pulumi.Input[int]]:
        """
        The initial capacity of the Auto Scaling group after the scheduled action runs and the capacity it attempts to maintain. Set to `-1` if you don't want to change the desired capacity at the scheduled time. Defaults to `0`.
        """
        return pulumi.get(self, "desired_capacity")

    @desired_capacity.setter
    def desired_capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "desired_capacity", value)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time for the recurring schedule to end, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        """
        return pulumi.get(self, "end_time")

    @end_time.setter
    def end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_time", value)

    @property
    @pulumi.getter(name="maxSize")
    def max_size(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum size of the Auto Scaling group. Set to `-1` if you don't want to change the maximum size at the scheduled time. Defaults to `0`.
        """
        return pulumi.get(self, "max_size")

    @max_size.setter
    def max_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_size", value)

    @property
    @pulumi.getter(name="minSize")
    def min_size(self) -> Optional[pulumi.Input[int]]:
        """
        The minimum size of the Auto Scaling group. Set to `-1` if you don't want to change the minimum size at the scheduled time. Defaults to `0`.
        """
        return pulumi.get(self, "min_size")

    @min_size.setter
    def min_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_size", value)

    @property
    @pulumi.getter
    def recurrence(self) -> Optional[pulumi.Input[str]]:
        """
        The recurring schedule for this action specified using the Unix cron syntax format.
        """
        return pulumi.get(self, "recurrence")

    @recurrence.setter
    def recurrence(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "recurrence", value)

    @property
    @pulumi.getter(name="scheduledActionName")
    def scheduled_action_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of this scaling action.

        The following arguments are optional:
        """
        return pulumi.get(self, "scheduled_action_name")

    @scheduled_action_name.setter
    def scheduled_action_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scheduled_action_name", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time for the recurring schedule to start, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_time", value)

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the time zone for a cron expression. Valid values are the canonical names of the IANA time zones (such as `Etc/GMT+9` or `Pacific/Tahiti`).

        > **NOTE:** When `start_time` and `end_time` are specified with `recurrence` , they form the boundaries of when the recurring action will start and stop.
        """
        return pulumi.get(self, "time_zone")

    @time_zone.setter
    def time_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "time_zone", value)


class Schedule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 autoscaling_group_name: Optional[pulumi.Input[str]] = None,
                 desired_capacity: Optional[pulumi.Input[int]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 max_size: Optional[pulumi.Input[int]] = None,
                 min_size: Optional[pulumi.Input[int]] = None,
                 recurrence: Optional[pulumi.Input[str]] = None,
                 scheduled_action_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an AutoScaling Schedule resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        foobar_group = aws.autoscaling.Group("foobarGroup",
            availability_zones=["us-west-2a"],
            max_size=1,
            min_size=1,
            health_check_grace_period=300,
            health_check_type="ELB",
            force_delete=True,
            termination_policies=["OldestInstance"])
        foobar_schedule = aws.autoscaling.Schedule("foobarSchedule",
            scheduled_action_name="foobar",
            min_size=0,
            max_size=1,
            desired_capacity=0,
            start_time="2016-12-11T18:00:00Z",
            end_time="2016-12-12T06:00:00Z",
            autoscaling_group_name=foobar_group.name)
        ```

        ## Import

        AutoScaling ScheduledAction can be imported using the `auto-scaling-group-name` and `scheduled-action-name`, e.g.,

        ```sh
         $ pulumi import aws:autoscaling/schedule:Schedule resource-name auto-scaling-group-name/scheduled-action-name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] autoscaling_group_name: The name of the Auto Scaling group.
        :param pulumi.Input[int] desired_capacity: The initial capacity of the Auto Scaling group after the scheduled action runs and the capacity it attempts to maintain. Set to `-1` if you don't want to change the desired capacity at the scheduled time. Defaults to `0`.
        :param pulumi.Input[str] end_time: The date and time for the recurring schedule to end, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        :param pulumi.Input[int] max_size: The maximum size of the Auto Scaling group. Set to `-1` if you don't want to change the maximum size at the scheduled time. Defaults to `0`.
        :param pulumi.Input[int] min_size: The minimum size of the Auto Scaling group. Set to `-1` if you don't want to change the minimum size at the scheduled time. Defaults to `0`.
        :param pulumi.Input[str] recurrence: The recurring schedule for this action specified using the Unix cron syntax format.
        :param pulumi.Input[str] scheduled_action_name: The name of this scaling action.
               
               The following arguments are optional:
        :param pulumi.Input[str] start_time: The date and time for the recurring schedule to start, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        :param pulumi.Input[str] time_zone: Specifies the time zone for a cron expression. Valid values are the canonical names of the IANA time zones (such as `Etc/GMT+9` or `Pacific/Tahiti`).
               
               > **NOTE:** When `start_time` and `end_time` are specified with `recurrence` , they form the boundaries of when the recurring action will start and stop.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ScheduleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an AutoScaling Schedule resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        foobar_group = aws.autoscaling.Group("foobarGroup",
            availability_zones=["us-west-2a"],
            max_size=1,
            min_size=1,
            health_check_grace_period=300,
            health_check_type="ELB",
            force_delete=True,
            termination_policies=["OldestInstance"])
        foobar_schedule = aws.autoscaling.Schedule("foobarSchedule",
            scheduled_action_name="foobar",
            min_size=0,
            max_size=1,
            desired_capacity=0,
            start_time="2016-12-11T18:00:00Z",
            end_time="2016-12-12T06:00:00Z",
            autoscaling_group_name=foobar_group.name)
        ```

        ## Import

        AutoScaling ScheduledAction can be imported using the `auto-scaling-group-name` and `scheduled-action-name`, e.g.,

        ```sh
         $ pulumi import aws:autoscaling/schedule:Schedule resource-name auto-scaling-group-name/scheduled-action-name
        ```

        :param str resource_name: The name of the resource.
        :param ScheduleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ScheduleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 autoscaling_group_name: Optional[pulumi.Input[str]] = None,
                 desired_capacity: Optional[pulumi.Input[int]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 max_size: Optional[pulumi.Input[int]] = None,
                 min_size: Optional[pulumi.Input[int]] = None,
                 recurrence: Optional[pulumi.Input[str]] = None,
                 scheduled_action_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ScheduleArgs.__new__(ScheduleArgs)

            if autoscaling_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'autoscaling_group_name'")
            __props__.__dict__["autoscaling_group_name"] = autoscaling_group_name
            __props__.__dict__["desired_capacity"] = desired_capacity
            __props__.__dict__["end_time"] = end_time
            __props__.__dict__["max_size"] = max_size
            __props__.__dict__["min_size"] = min_size
            __props__.__dict__["recurrence"] = recurrence
            if scheduled_action_name is None and not opts.urn:
                raise TypeError("Missing required property 'scheduled_action_name'")
            __props__.__dict__["scheduled_action_name"] = scheduled_action_name
            __props__.__dict__["start_time"] = start_time
            __props__.__dict__["time_zone"] = time_zone
            __props__.__dict__["arn"] = None
        super(Schedule, __self__).__init__(
            'aws:autoscaling/schedule:Schedule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            autoscaling_group_name: Optional[pulumi.Input[str]] = None,
            desired_capacity: Optional[pulumi.Input[int]] = None,
            end_time: Optional[pulumi.Input[str]] = None,
            max_size: Optional[pulumi.Input[int]] = None,
            min_size: Optional[pulumi.Input[int]] = None,
            recurrence: Optional[pulumi.Input[str]] = None,
            scheduled_action_name: Optional[pulumi.Input[str]] = None,
            start_time: Optional[pulumi.Input[str]] = None,
            time_zone: Optional[pulumi.Input[str]] = None) -> 'Schedule':
        """
        Get an existing Schedule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN assigned by AWS to the autoscaling schedule.
        :param pulumi.Input[str] autoscaling_group_name: The name of the Auto Scaling group.
        :param pulumi.Input[int] desired_capacity: The initial capacity of the Auto Scaling group after the scheduled action runs and the capacity it attempts to maintain. Set to `-1` if you don't want to change the desired capacity at the scheduled time. Defaults to `0`.
        :param pulumi.Input[str] end_time: The date and time for the recurring schedule to end, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        :param pulumi.Input[int] max_size: The maximum size of the Auto Scaling group. Set to `-1` if you don't want to change the maximum size at the scheduled time. Defaults to `0`.
        :param pulumi.Input[int] min_size: The minimum size of the Auto Scaling group. Set to `-1` if you don't want to change the minimum size at the scheduled time. Defaults to `0`.
        :param pulumi.Input[str] recurrence: The recurring schedule for this action specified using the Unix cron syntax format.
        :param pulumi.Input[str] scheduled_action_name: The name of this scaling action.
               
               The following arguments are optional:
        :param pulumi.Input[str] start_time: The date and time for the recurring schedule to start, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        :param pulumi.Input[str] time_zone: Specifies the time zone for a cron expression. Valid values are the canonical names of the IANA time zones (such as `Etc/GMT+9` or `Pacific/Tahiti`).
               
               > **NOTE:** When `start_time` and `end_time` are specified with `recurrence` , they form the boundaries of when the recurring action will start and stop.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ScheduleState.__new__(_ScheduleState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["autoscaling_group_name"] = autoscaling_group_name
        __props__.__dict__["desired_capacity"] = desired_capacity
        __props__.__dict__["end_time"] = end_time
        __props__.__dict__["max_size"] = max_size
        __props__.__dict__["min_size"] = min_size
        __props__.__dict__["recurrence"] = recurrence
        __props__.__dict__["scheduled_action_name"] = scheduled_action_name
        __props__.__dict__["start_time"] = start_time
        __props__.__dict__["time_zone"] = time_zone
        return Schedule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN assigned by AWS to the autoscaling schedule.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoscalingGroupName")
    def autoscaling_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Auto Scaling group.
        """
        return pulumi.get(self, "autoscaling_group_name")

    @property
    @pulumi.getter(name="desiredCapacity")
    def desired_capacity(self) -> pulumi.Output[int]:
        """
        The initial capacity of the Auto Scaling group after the scheduled action runs and the capacity it attempts to maintain. Set to `-1` if you don't want to change the desired capacity at the scheduled time. Defaults to `0`.
        """
        return pulumi.get(self, "desired_capacity")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[str]:
        """
        The date and time for the recurring schedule to end, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="maxSize")
    def max_size(self) -> pulumi.Output[int]:
        """
        The maximum size of the Auto Scaling group. Set to `-1` if you don't want to change the maximum size at the scheduled time. Defaults to `0`.
        """
        return pulumi.get(self, "max_size")

    @property
    @pulumi.getter(name="minSize")
    def min_size(self) -> pulumi.Output[int]:
        """
        The minimum size of the Auto Scaling group. Set to `-1` if you don't want to change the minimum size at the scheduled time. Defaults to `0`.
        """
        return pulumi.get(self, "min_size")

    @property
    @pulumi.getter
    def recurrence(self) -> pulumi.Output[str]:
        """
        The recurring schedule for this action specified using the Unix cron syntax format.
        """
        return pulumi.get(self, "recurrence")

    @property
    @pulumi.getter(name="scheduledActionName")
    def scheduled_action_name(self) -> pulumi.Output[str]:
        """
        The name of this scaling action.

        The following arguments are optional:
        """
        return pulumi.get(self, "scheduled_action_name")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[str]:
        """
        The date and time for the recurring schedule to start, in UTC with the format `"YYYY-MM-DDThh:mm:ssZ"` (e.g. `"2021-06-01T00:00:00Z"`).
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> pulumi.Output[str]:
        """
        Specifies the time zone for a cron expression. Valid values are the canonical names of the IANA time zones (such as `Etc/GMT+9` or `Pacific/Tahiti`).

        > **NOTE:** When `start_time` and `end_time` are specified with `recurrence` , they form the boundaries of when the recurring action will start and stop.
        """
        return pulumi.get(self, "time_zone")

