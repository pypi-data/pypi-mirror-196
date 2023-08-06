# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from functools import total_ordering
from typing import Union
from uuid import uuid4

import numpy as np

from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (INFINITY,
                                                                 DataSetType)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager


@total_ordering
class Interval:
    def __init__(self, field: Union[str, int, float]) -> None:
        self.id = str(uuid4())
        self.field = field
        self.values = []
        self._absolute_change_percentage = -1
        self._eligible_for_insights = None
        self.insights_available = False

    @property
    def absolute_change_percentage(self) -> float:
        if self._absolute_change_percentage == -1:
            self._absolute_change_percentage = self._calculate_absolute_change_percentage()
        return self._absolute_change_percentage

    @property
    def is_change_significant(self) -> bool:
        return True

    @property
    def eligible_for_insights(self) -> bool:
        if self._eligible_for_insights is not None:
            return self._eligible_for_insights

        threshold = ControlBoxManager().get_control_box().get_interval_count_insights_threshold()
        # Calculate insights only if either of  baseline/production percentages > threshold.
        self._eligible_for_insights = (
            self.values[0].percentage >= threshold) or (
            self.values[1].percentage >= threshold)
        return self._eligible_for_insights

    def _calculate_absolute_change_percentage(self) -> float:
        if len(self.values) != 2:
            return -1

        baseline_value = next(
            value for value in self.values if value.type == DataSetType.BASELINE)
        production_value = next(
            value for value in self.values if value.type == DataSetType.PRODUCTION)

        if (baseline_value is None) or (production_value is None):
            return -1

        if baseline_value.absolute_count == 0:
            return INFINITY

        return np.abs(
            (production_value.percentage -
             baseline_value.percentage) /
            baseline_value.percentage)

    def add_baseline_value(self, absolute_count: int, percentage: float) -> None:
        self.values.append(IntervalValue(DataSetType.BASELINE, absolute_count, percentage))

    def add_production_value(self, absolute_count: int, percentage: float) -> None:
        self.values.append(IntervalValue(
            DataSetType.PRODUCTION, absolute_count, percentage))

    def get_baseline_value(self) -> "IntervalValue":
        return next(value for value in self.values if value.type == DataSetType.BASELINE)

    def get_production_value(self) -> "IntervalValue":
        return next(value for value in self.values if value.type == DataSetType.PRODUCTION)

    def has_increased_in_production(self) -> bool:
        baseline = self.get_baseline_value()
        production = self.get_production_value()

        return production.percentage > baseline.percentage

    def __lt__(self, other) -> bool:
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        raise NotImplementedError

    def to_dict(self) -> dict:
        return {
            "id": get_python_types(self.id),
            "field": get_python_types(
                self.field),
            "absolute_change_percentage": get_python_types(
                self.absolute_change_percentage),
            "eligible_for_insights": get_python_types(
                self.eligible_for_insights),
            "insights_available": get_python_types(
                self.insights_available),
            "is_change_significant": get_python_types(self.is_change_significant),
            "increased_in_production": get_python_types(self.has_increased_in_production()),
            "baseline_absolute_count": get_python_types(self.get_baseline_value().absolute_count),
            "baseline_percentage": get_python_types(self.get_baseline_value().percentage),
            "production_absolute_count": get_python_types(self.get_production_value().absolute_count),
            "production_percentage": get_python_types(self.get_production_value().percentage)
        }

    @classmethod
    def from_dict(cls, dict_: dict) -> "Interval":
        raise NotImplementedError


class ContinuousStatisticsInterval(Interval):
    def __init__(self, lower_bound: Union[int, float], upper_bound: Union[int, float]) -> None:
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        super().__init__(f"{lower_bound}-{upper_bound}")

    def __lt__(self, other) -> bool:
        if self.absolute_change_percentage == other.absolute_change_percentage:
            if self.lower_bound == other.lower_bound:
                return self.upper_bound < other.upper_bound
            return self.lower_bound < other.lower_bound

        return self.absolute_change_percentage < other.absolute_change_percentage

    def __eq__(self, other) -> bool:
        return self.absolute_change_percentage == other.absolute_change_percentage and \
            self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_["lower_bound"] = get_python_types(self.lower_bound)
        dict_["upper_bound"] = get_python_types(self.upper_bound)
        return dict_

    @classmethod
    def from_dict(cls, dict_: dict) -> "ContinuousStatisticsInterval":
        try:
            interval = ContinuousStatisticsInterval(
                dict_["lower_bound"], dict_["upper_bound"])
            interval.id = dict_["id"]
            interval.add_baseline_value(
                absolute_count=dict_["baseline_absolute_count"],
                percentage=dict_["baseline_percentage"])
            interval.add_production_value(
                absolute_count=dict_["production_absolute_count"],
                percentage=dict_["production_percentage"])

            _ = interval.absolute_change_percentage

            interval.eligible_for_insights = dict_["eligible_for_insights"]
            interval.insights_available = dict_["insights_available"]
            return interval
        except KeyError as e:
            raise ValueError(f"Missing key {e} in dict {dict_}") from e


class DiscreteStatisticsInterval(Interval):
    def __init__(self, field: Union[str, int, float]) -> None:
        super().__init__(field)
        self.contribution_to_distance = -1
        self.statistical_buffer = -1

    @property
    def is_change_significant(self) -> bool:
        return bool(self.absolute_change_percentage and (
            self.absolute_change_percentage > self.statistical_buffer))

    def __lt__(self, other) -> bool:
        if self.absolute_change_percentage == other.absolute_change_percentage:
            return self.contribution_to_distance < other.contribution_to_distance
        return self.absolute_change_percentage < other.absolute_change_percentage

    def __eq__(self, other) -> bool:
        return (self.absolute_change_percentage == other.absolute_change_percentage) \
            and (self.contribution_to_distance == other.contribution_to_distance)

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_["contribution_to_distance"] = get_python_types(self.contribution_to_distance)
        dict_["statistical_buffer"] = get_python_types(self.statistical_buffer)
        return dict_

    @classmethod
    def from_dict(cls, dict_: dict) -> "DiscreteStatisticsInterval":
        try:
            interval = DiscreteStatisticsInterval(dict_["field"])
            interval.id = dict_["id"]
            interval.add_baseline_value(
                absolute_count=dict_["baseline_absolute_count"],
                percentage=dict_["baseline_percentage"])
            interval.add_production_value(
                absolute_count=dict_["production_absolute_count"],
                percentage=dict_["production_percentage"])

            interval.contribution_to_distance = dict_[
                "contribution_to_distance"]
            interval.statistical_buffer = dict_["statistical_buffer"]
            _ = interval.absolute_change_percentage
            interval.eligible_for_insights = dict_["eligible_for_insights"]
            interval.insights_available = dict_["insights_available"]
            return interval

        except KeyError as e:
            raise ValueError(f"Invalid interval dict: {dict_}") from e


class IntervalValue:
    def __init__(self, type: DataSetType, absolute_count: int, percentage: float) -> None:
        self.type = type
        self.absolute_count = absolute_count
        self.percentage = percentage
