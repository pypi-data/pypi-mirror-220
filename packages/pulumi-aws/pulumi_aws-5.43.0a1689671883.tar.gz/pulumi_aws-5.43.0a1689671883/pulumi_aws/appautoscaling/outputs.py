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

__all__ = [
    'PolicyStepScalingPolicyConfiguration',
    'PolicyStepScalingPolicyConfigurationStepAdjustment',
    'PolicyTargetTrackingScalingPolicyConfiguration',
    'PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecification',
    'PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationDimension',
    'PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetric',
    'PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStat',
    'PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetric',
    'PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetricDimension',
    'PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecification',
    'ScheduledActionScalableTargetAction',
]

@pulumi.output_type
class PolicyStepScalingPolicyConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "adjustmentType":
            suggest = "adjustment_type"
        elif key == "metricAggregationType":
            suggest = "metric_aggregation_type"
        elif key == "minAdjustmentMagnitude":
            suggest = "min_adjustment_magnitude"
        elif key == "stepAdjustments":
            suggest = "step_adjustments"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyStepScalingPolicyConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyStepScalingPolicyConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyStepScalingPolicyConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 adjustment_type: Optional[str] = None,
                 cooldown: Optional[int] = None,
                 metric_aggregation_type: Optional[str] = None,
                 min_adjustment_magnitude: Optional[int] = None,
                 step_adjustments: Optional[Sequence['outputs.PolicyStepScalingPolicyConfigurationStepAdjustment']] = None):
        """
        :param str adjustment_type: Whether the adjustment is an absolute number or a percentage of the current capacity. Valid values are `ChangeInCapacity`, `ExactCapacity`, and `PercentChangeInCapacity`.
        :param int cooldown: Amount of time, in seconds, after a scaling activity completes and before the next scaling activity can start.
        :param str metric_aggregation_type: Aggregation type for the policy's metrics. Valid values are "Minimum", "Maximum", and "Average". Without a value, AWS will treat the aggregation type as "Average".
        :param int min_adjustment_magnitude: Minimum number to adjust your scalable dimension as a result of a scaling activity. If the adjustment type is PercentChangeInCapacity, the scaling policy changes the scalable dimension of the scalable target by this amount.
        :param Sequence['PolicyStepScalingPolicyConfigurationStepAdjustmentArgs'] step_adjustments: Set of adjustments that manage scaling. These have the following structure:
               
               ```python
               import pulumi
               import pulumi_aws as aws
               
               ecs_policy = aws.appautoscaling.Policy("ecsPolicy", step_scaling_policy_configuration=aws.appautoscaling.PolicyStepScalingPolicyConfigurationArgs(
                   step_adjustments=[
                       aws.appautoscaling.PolicyStepScalingPolicyConfigurationStepAdjustmentArgs(
                           metric_interval_lower_bound="1",
                           metric_interval_upper_bound="2",
                           scaling_adjustment=-1,
                       ),
                       aws.appautoscaling.PolicyStepScalingPolicyConfigurationStepAdjustmentArgs(
                           metric_interval_lower_bound="2",
                           metric_interval_upper_bound="3",
                           scaling_adjustment=1,
                       ),
                   ],
               ))
               ```
        """
        if adjustment_type is not None:
            pulumi.set(__self__, "adjustment_type", adjustment_type)
        if cooldown is not None:
            pulumi.set(__self__, "cooldown", cooldown)
        if metric_aggregation_type is not None:
            pulumi.set(__self__, "metric_aggregation_type", metric_aggregation_type)
        if min_adjustment_magnitude is not None:
            pulumi.set(__self__, "min_adjustment_magnitude", min_adjustment_magnitude)
        if step_adjustments is not None:
            pulumi.set(__self__, "step_adjustments", step_adjustments)

    @property
    @pulumi.getter(name="adjustmentType")
    def adjustment_type(self) -> Optional[str]:
        """
        Whether the adjustment is an absolute number or a percentage of the current capacity. Valid values are `ChangeInCapacity`, `ExactCapacity`, and `PercentChangeInCapacity`.
        """
        return pulumi.get(self, "adjustment_type")

    @property
    @pulumi.getter
    def cooldown(self) -> Optional[int]:
        """
        Amount of time, in seconds, after a scaling activity completes and before the next scaling activity can start.
        """
        return pulumi.get(self, "cooldown")

    @property
    @pulumi.getter(name="metricAggregationType")
    def metric_aggregation_type(self) -> Optional[str]:
        """
        Aggregation type for the policy's metrics. Valid values are "Minimum", "Maximum", and "Average". Without a value, AWS will treat the aggregation type as "Average".
        """
        return pulumi.get(self, "metric_aggregation_type")

    @property
    @pulumi.getter(name="minAdjustmentMagnitude")
    def min_adjustment_magnitude(self) -> Optional[int]:
        """
        Minimum number to adjust your scalable dimension as a result of a scaling activity. If the adjustment type is PercentChangeInCapacity, the scaling policy changes the scalable dimension of the scalable target by this amount.
        """
        return pulumi.get(self, "min_adjustment_magnitude")

    @property
    @pulumi.getter(name="stepAdjustments")
    def step_adjustments(self) -> Optional[Sequence['outputs.PolicyStepScalingPolicyConfigurationStepAdjustment']]:
        """
        Set of adjustments that manage scaling. These have the following structure:

        ```python
        import pulumi
        import pulumi_aws as aws

        ecs_policy = aws.appautoscaling.Policy("ecsPolicy", step_scaling_policy_configuration=aws.appautoscaling.PolicyStepScalingPolicyConfigurationArgs(
            step_adjustments=[
                aws.appautoscaling.PolicyStepScalingPolicyConfigurationStepAdjustmentArgs(
                    metric_interval_lower_bound="1",
                    metric_interval_upper_bound="2",
                    scaling_adjustment=-1,
                ),
                aws.appautoscaling.PolicyStepScalingPolicyConfigurationStepAdjustmentArgs(
                    metric_interval_lower_bound="2",
                    metric_interval_upper_bound="3",
                    scaling_adjustment=1,
                ),
            ],
        ))
        ```
        """
        return pulumi.get(self, "step_adjustments")


@pulumi.output_type
class PolicyStepScalingPolicyConfigurationStepAdjustment(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "scalingAdjustment":
            suggest = "scaling_adjustment"
        elif key == "metricIntervalLowerBound":
            suggest = "metric_interval_lower_bound"
        elif key == "metricIntervalUpperBound":
            suggest = "metric_interval_upper_bound"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyStepScalingPolicyConfigurationStepAdjustment. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyStepScalingPolicyConfigurationStepAdjustment.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyStepScalingPolicyConfigurationStepAdjustment.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 scaling_adjustment: int,
                 metric_interval_lower_bound: Optional[str] = None,
                 metric_interval_upper_bound: Optional[str] = None):
        """
        :param int scaling_adjustment: Number of members by which to scale, when the adjustment bounds are breached. A positive value scales up. A negative value scales down.
        :param str metric_interval_lower_bound: Lower bound for the difference between the alarm threshold and the CloudWatch metric. Without a value, AWS will treat this bound as negative infinity.
        :param str metric_interval_upper_bound: Upper bound for the difference between the alarm threshold and the CloudWatch metric. Without a value, AWS will treat this bound as infinity. The upper bound must be greater than the lower bound.
        """
        pulumi.set(__self__, "scaling_adjustment", scaling_adjustment)
        if metric_interval_lower_bound is not None:
            pulumi.set(__self__, "metric_interval_lower_bound", metric_interval_lower_bound)
        if metric_interval_upper_bound is not None:
            pulumi.set(__self__, "metric_interval_upper_bound", metric_interval_upper_bound)

    @property
    @pulumi.getter(name="scalingAdjustment")
    def scaling_adjustment(self) -> int:
        """
        Number of members by which to scale, when the adjustment bounds are breached. A positive value scales up. A negative value scales down.
        """
        return pulumi.get(self, "scaling_adjustment")

    @property
    @pulumi.getter(name="metricIntervalLowerBound")
    def metric_interval_lower_bound(self) -> Optional[str]:
        """
        Lower bound for the difference between the alarm threshold and the CloudWatch metric. Without a value, AWS will treat this bound as negative infinity.
        """
        return pulumi.get(self, "metric_interval_lower_bound")

    @property
    @pulumi.getter(name="metricIntervalUpperBound")
    def metric_interval_upper_bound(self) -> Optional[str]:
        """
        Upper bound for the difference between the alarm threshold and the CloudWatch metric. Without a value, AWS will treat this bound as infinity. The upper bound must be greater than the lower bound.
        """
        return pulumi.get(self, "metric_interval_upper_bound")


@pulumi.output_type
class PolicyTargetTrackingScalingPolicyConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "targetValue":
            suggest = "target_value"
        elif key == "customizedMetricSpecification":
            suggest = "customized_metric_specification"
        elif key == "disableScaleIn":
            suggest = "disable_scale_in"
        elif key == "predefinedMetricSpecification":
            suggest = "predefined_metric_specification"
        elif key == "scaleInCooldown":
            suggest = "scale_in_cooldown"
        elif key == "scaleOutCooldown":
            suggest = "scale_out_cooldown"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyTargetTrackingScalingPolicyConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyTargetTrackingScalingPolicyConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyTargetTrackingScalingPolicyConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 target_value: float,
                 customized_metric_specification: Optional['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecification'] = None,
                 disable_scale_in: Optional[bool] = None,
                 predefined_metric_specification: Optional['outputs.PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecification'] = None,
                 scale_in_cooldown: Optional[int] = None,
                 scale_out_cooldown: Optional[int] = None):
        """
        :param float target_value: Target value for the metric.
        :param 'PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationArgs' customized_metric_specification: Custom CloudWatch metric. Documentation can be found  at: [AWS Customized Metric Specification](https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_CustomizedMetricSpecification.html). See supported fields below.
        :param bool disable_scale_in: Whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. The default value is `false`.
        :param 'PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecificationArgs' predefined_metric_specification: Predefined metric. See supported fields below.
        :param int scale_in_cooldown: Amount of time, in seconds, after a scale in activity completes before another scale in activity can start.
        :param int scale_out_cooldown: Amount of time, in seconds, after a scale out activity completes before another scale out activity can start.
        """
        pulumi.set(__self__, "target_value", target_value)
        if customized_metric_specification is not None:
            pulumi.set(__self__, "customized_metric_specification", customized_metric_specification)
        if disable_scale_in is not None:
            pulumi.set(__self__, "disable_scale_in", disable_scale_in)
        if predefined_metric_specification is not None:
            pulumi.set(__self__, "predefined_metric_specification", predefined_metric_specification)
        if scale_in_cooldown is not None:
            pulumi.set(__self__, "scale_in_cooldown", scale_in_cooldown)
        if scale_out_cooldown is not None:
            pulumi.set(__self__, "scale_out_cooldown", scale_out_cooldown)

    @property
    @pulumi.getter(name="targetValue")
    def target_value(self) -> float:
        """
        Target value for the metric.
        """
        return pulumi.get(self, "target_value")

    @property
    @pulumi.getter(name="customizedMetricSpecification")
    def customized_metric_specification(self) -> Optional['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecification']:
        """
        Custom CloudWatch metric. Documentation can be found  at: [AWS Customized Metric Specification](https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_CustomizedMetricSpecification.html). See supported fields below.
        """
        return pulumi.get(self, "customized_metric_specification")

    @property
    @pulumi.getter(name="disableScaleIn")
    def disable_scale_in(self) -> Optional[bool]:
        """
        Whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. The default value is `false`.
        """
        return pulumi.get(self, "disable_scale_in")

    @property
    @pulumi.getter(name="predefinedMetricSpecification")
    def predefined_metric_specification(self) -> Optional['outputs.PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecification']:
        """
        Predefined metric. See supported fields below.
        """
        return pulumi.get(self, "predefined_metric_specification")

    @property
    @pulumi.getter(name="scaleInCooldown")
    def scale_in_cooldown(self) -> Optional[int]:
        """
        Amount of time, in seconds, after a scale in activity completes before another scale in activity can start.
        """
        return pulumi.get(self, "scale_in_cooldown")

    @property
    @pulumi.getter(name="scaleOutCooldown")
    def scale_out_cooldown(self) -> Optional[int]:
        """
        Amount of time, in seconds, after a scale out activity completes before another scale out activity can start.
        """
        return pulumi.get(self, "scale_out_cooldown")


@pulumi.output_type
class PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecification(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricName":
            suggest = "metric_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecification. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecification.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecification.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 dimensions: Optional[Sequence['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationDimension']] = None,
                 metric_name: Optional[str] = None,
                 metrics: Optional[Sequence['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetric']] = None,
                 namespace: Optional[str] = None,
                 statistic: Optional[str] = None,
                 unit: Optional[str] = None):
        """
        :param Sequence['PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationDimensionArgs'] dimensions: Configuration block(s) with the dimensions of the metric if the metric was published with dimensions. Detailed below.
        :param str metric_name: Name of the metric.
        :param Sequence['PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricArgs'] metrics: Metrics to include, as a metric data query.
        :param str namespace: Namespace of the metric.
        :param str statistic: Statistic of the metric. Valid values: `Average`, `Minimum`, `Maximum`, `SampleCount`, and `Sum`.
        :param str unit: Unit of the metric.
        """
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)
        if metric_name is not None:
            pulumi.set(__self__, "metric_name", metric_name)
        if metrics is not None:
            pulumi.set(__self__, "metrics", metrics)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if statistic is not None:
            pulumi.set(__self__, "statistic", statistic)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationDimension']]:
        """
        Configuration block(s) with the dimensions of the metric if the metric was published with dimensions. Detailed below.
        """
        return pulumi.get(self, "dimensions")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> Optional[str]:
        """
        Name of the metric.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def metrics(self) -> Optional[Sequence['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetric']]:
        """
        Metrics to include, as a metric data query.
        """
        return pulumi.get(self, "metrics")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        """
        Namespace of the metric.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def statistic(self) -> Optional[str]:
        """
        Statistic of the metric. Valid values: `Average`, `Minimum`, `Maximum`, `SampleCount`, and `Sum`.
        """
        return pulumi.get(self, "statistic")

    @property
    @pulumi.getter
    def unit(self) -> Optional[str]:
        """
        Unit of the metric.
        """
        return pulumi.get(self, "unit")


@pulumi.output_type
class PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationDimension(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        :param str name: Name of the policy. Must be between 1 and 255 characters in length.
        :param str value: Value of the dimension.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the policy. Must be between 1 and 255 characters in length.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the dimension.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetric(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricStat":
            suggest = "metric_stat"
        elif key == "returnData":
            suggest = "return_data"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetric. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetric.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetric.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 expression: Optional[str] = None,
                 label: Optional[str] = None,
                 metric_stat: Optional['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStat'] = None,
                 return_data: Optional[bool] = None):
        """
        :param str id: Short name for the metric used in target tracking scaling policy.
        :param str expression: Math expression used on the returned metric. You must specify either `expression` or `metric_stat`, but not both.
        :param str label: Human-readable label for this metric or expression.
        :param 'PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatArgs' metric_stat: Structure that defines CloudWatch metric to be used in target tracking scaling policy. You must specify either `expression` or `metric_stat`, but not both.
        :param bool return_data: Boolean that indicates whether to return the timestamps and raw data values of this metric, the default is true
        """
        pulumi.set(__self__, "id", id)
        if expression is not None:
            pulumi.set(__self__, "expression", expression)
        if label is not None:
            pulumi.set(__self__, "label", label)
        if metric_stat is not None:
            pulumi.set(__self__, "metric_stat", metric_stat)
        if return_data is not None:
            pulumi.set(__self__, "return_data", return_data)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Short name for the metric used in target tracking scaling policy.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def expression(self) -> Optional[str]:
        """
        Math expression used on the returned metric. You must specify either `expression` or `metric_stat`, but not both.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def label(self) -> Optional[str]:
        """
        Human-readable label for this metric or expression.
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter(name="metricStat")
    def metric_stat(self) -> Optional['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStat']:
        """
        Structure that defines CloudWatch metric to be used in target tracking scaling policy. You must specify either `expression` or `metric_stat`, but not both.
        """
        return pulumi.get(self, "metric_stat")

    @property
    @pulumi.getter(name="returnData")
    def return_data(self) -> Optional[bool]:
        """
        Boolean that indicates whether to return the timestamps and raw data values of this metric, the default is true
        """
        return pulumi.get(self, "return_data")


@pulumi.output_type
class PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStat(dict):
    def __init__(__self__, *,
                 metric: 'outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetric',
                 stat: str,
                 unit: Optional[str] = None):
        """
        :param 'PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetricArgs' metric: Structure that defines the CloudWatch metric to return, including the metric name, namespace, and dimensions.
        :param str stat: Statistic of the metrics to return.
        :param str unit: Unit of the metric.
        """
        pulumi.set(__self__, "metric", metric)
        pulumi.set(__self__, "stat", stat)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter
    def metric(self) -> 'outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetric':
        """
        Structure that defines the CloudWatch metric to return, including the metric name, namespace, and dimensions.
        """
        return pulumi.get(self, "metric")

    @property
    @pulumi.getter
    def stat(self) -> str:
        """
        Statistic of the metrics to return.
        """
        return pulumi.get(self, "stat")

    @property
    @pulumi.getter
    def unit(self) -> Optional[str]:
        """
        Unit of the metric.
        """
        return pulumi.get(self, "unit")


@pulumi.output_type
class PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetric(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "metricName":
            suggest = "metric_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetric. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetric.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetric.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 metric_name: str,
                 namespace: str,
                 dimensions: Optional[Sequence['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetricDimension']] = None):
        """
        :param str metric_name: Name of the metric.
        :param str namespace: Namespace of the metric.
        :param Sequence['PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetricDimensionArgs'] dimensions: Configuration block(s) with the dimensions of the metric if the metric was published with dimensions. Detailed below.
        """
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "namespace", namespace)
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> str:
        """
        Name of the metric.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def namespace(self) -> str:
        """
        Namespace of the metric.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetricDimension']]:
        """
        Configuration block(s) with the dimensions of the metric if the metric was published with dimensions. Detailed below.
        """
        return pulumi.get(self, "dimensions")


@pulumi.output_type
class PolicyTargetTrackingScalingPolicyConfigurationCustomizedMetricSpecificationMetricMetricStatMetricDimension(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        :param str name: Name of the policy. Must be between 1 and 255 characters in length.
        :param str value: Value of the dimension.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the policy. Must be between 1 and 255 characters in length.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the dimension.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecification(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "predefinedMetricType":
            suggest = "predefined_metric_type"
        elif key == "resourceLabel":
            suggest = "resource_label"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecification. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecification.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecification.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 predefined_metric_type: str,
                 resource_label: Optional[str] = None):
        """
        :param str predefined_metric_type: Metric type.
        :param str resource_label: Reserved for future use if the `predefined_metric_type` is not `ALBRequestCountPerTarget`. If the `predefined_metric_type` is `ALBRequestCountPerTarget`, you must specify this argument. Documentation can be found at: [AWS Predefined Scaling Metric Specification](https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_PredefinedScalingMetricSpecification.html). Must be less than or equal to 1023 characters in length.
        """
        pulumi.set(__self__, "predefined_metric_type", predefined_metric_type)
        if resource_label is not None:
            pulumi.set(__self__, "resource_label", resource_label)

    @property
    @pulumi.getter(name="predefinedMetricType")
    def predefined_metric_type(self) -> str:
        """
        Metric type.
        """
        return pulumi.get(self, "predefined_metric_type")

    @property
    @pulumi.getter(name="resourceLabel")
    def resource_label(self) -> Optional[str]:
        """
        Reserved for future use if the `predefined_metric_type` is not `ALBRequestCountPerTarget`. If the `predefined_metric_type` is `ALBRequestCountPerTarget`, you must specify this argument. Documentation can be found at: [AWS Predefined Scaling Metric Specification](https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_PredefinedScalingMetricSpecification.html). Must be less than or equal to 1023 characters in length.
        """
        return pulumi.get(self, "resource_label")


@pulumi.output_type
class ScheduledActionScalableTargetAction(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "maxCapacity":
            suggest = "max_capacity"
        elif key == "minCapacity":
            suggest = "min_capacity"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScheduledActionScalableTargetAction. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScheduledActionScalableTargetAction.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScheduledActionScalableTargetAction.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 max_capacity: Optional[int] = None,
                 min_capacity: Optional[int] = None):
        """
        :param int max_capacity: Maximum capacity. At least one of `max_capacity` or `min_capacity` must be set.
        :param int min_capacity: Minimum capacity. At least one of `min_capacity` or `max_capacity` must be set.
        """
        if max_capacity is not None:
            pulumi.set(__self__, "max_capacity", max_capacity)
        if min_capacity is not None:
            pulumi.set(__self__, "min_capacity", min_capacity)

    @property
    @pulumi.getter(name="maxCapacity")
    def max_capacity(self) -> Optional[int]:
        """
        Maximum capacity. At least one of `max_capacity` or `min_capacity` must be set.
        """
        return pulumi.get(self, "max_capacity")

    @property
    @pulumi.getter(name="minCapacity")
    def min_capacity(self) -> Optional[int]:
        """
        Minimum capacity. At least one of `min_capacity` or `max_capacity` must be set.
        """
        return pulumi.get(self, "min_capacity")


