# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022, 2023
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import json
import pickle
from abc import abstractmethod
from datetime import datetime
from itertools import product
from typing import Dict, List, Tuple, Union
from uuid import uuid4

import numpy as np
import pandas as pd
import sqlalchemy
from tqdm import tqdm

from ibm_metrics_plugin.common.utils.constants import ProblemType
from ibm_metrics_plugin.common.utils.datetime_util import DateTimeUtil
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.common.utils.python_utils import (get,
                                                          get_python_types,
                                                          is_exists)
from ibm_metrics_plugin.metrics.drift_v2.entity.column.categorical_column import \
    CategoricalColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.column.numerical_column import \
    NumericalColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.data_quality.data_quality_issue import \
    DataQualityIssue
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.connection.connection_details import \
    Connection
from ibm_metrics_plugin.metrics.drift_v2.entity.operation.operation import \
    Operation
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.statistics import \
    Statistics
from ibm_metrics_plugin.metrics.drift_v2.utils.async_utils import \
    gather_with_concurrency
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    PROBABILITY_COLUMN_TEMPLATE, RANDOM_SEED, ColumnRole, DataQualityIssueKind,
    DataSetType, OperationKind)
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import (
    ControlBox, ControlBoxManager)
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


class DriftDataSet:
    """Parent class for all types of datasets.

    Possible use cases:
    - [x] Training Data + Scoring Fn + Pandas DataFrame
    - [x] Scored Training Data + Pandas DataFrame
    - [x] Scored Training Data + SQLAlchemy Connection
    - [x] Payload Data + SQLAlchemy Connection
    - [] Scored Training Data + Spark Session [Not in Phase 1]

    """

    np.random.seed(RANDOM_SEED)

    def __init__(self, data_set_type: DataSetType):
        self.id = str(uuid4())
        self.version = "0.0.1"

        self.type = data_set_type
        self.count = None

        # Version History
        # 0.0.1 - Initial version

        self.columns = {}
        self.operations = {}
        self.data_quality_issues = {}
        self.data_quality_violations = {}
        self.unique_labels = []
        self.predicted_labels = []
        self.probability_column = None
        self.problem_type = None
        self.advanced_controls = {}
        self.has_model_quality_drift = False
        self.has_data_quality_issues = False
        self.meta_model = None
        self.max_samples = None

    @classmethod
    async def factory(self,
                      data: Union[pd.DataFrame, dict],
                      data_set_type: DataSetType,
                      problem_type: ProblemType,
                      feature_columns: List[str],
                      feature_importance: dict,
                      categorical_columns: List[str] = [],
                      label_column: str = None,
                      prediction_column: str = None,
                      probability_column: str = None,
                      max_samples: int = None,
                      scoring_fn: callable = None,
                      advanced_controls: dict = {},) -> "DriftDataSet":
        """Factory method to create a DriftDataSet.

        Args:
            data (Union[pd.DataFrame, dict]): The data to use.
            data_set_type (DataSetType): The type of the data set.
            problem_type (ProblemType): The problem type.
            feature_columns (List[str]): The list of feature columns.
            feature_importance (dict): The feature importance.
            categorical_columns (List[str], optional): The list of categorical columns. Defaults to [].
            label_column (str, optional): The label column. Defaults to None.
            prediction_column (str, optional): The prediction column. Defaults to None.
            probability_column (str, optional): The probability column. Defaults to None.
            scoring_fn (callable, optional): The scoring function. Accepts a dataframe with features as columns and
                returns a tuple of numpy array of probabilities array of shape `(n_samples,n_classes)` and numpy
                array of prediction vector of shape `(n_samples,)`. Defaults to None.

        Returns:
            DriftDataSet: The dataset.
        """
        if isinstance(data, pd.DataFrame):
            from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.pandas_data_set import \
                PandasDataSet
            data_set = PandasDataSet(data_set_type)
        elif isinstance(data, dict):
            from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.sql_data_set import \
                SqlDataSet
            data_set = SqlDataSet(data_set_type)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

        await data_set.initialize(
            data=data,
            problem_type=problem_type,
            feature_columns=feature_columns,
            feature_importance=feature_importance,
            categorical_columns=categorical_columns,
            label_column=label_column,
            prediction_column=prediction_column,
            probability_column=probability_column,
            max_samples=max_samples,
            scoring_fn=scoring_fn,
            advanced_controls=advanced_controls)

        return data_set

    @abstractmethod
    async def initialize(self,
                         data: Union[pd.DataFrame, sqlalchemy.engine.base.Engine],
                         problem_type: ProblemType,
                         feature_columns: List[str],
                         feature_importance: dict,
                         categorical_columns: List[str] = [],
                         label_column: str = None,
                         prediction_column: str = None,
                         probability_column: str = None,
                         max_samples: int = None,
                         scoring_fn: callable = None,
                         advanced_controls: dict = {}):
        """Initialize the dataset with columns, operations etc.

        Args:
            data (Union[pd.DataFrame, sqlalchemy.engine.base.Engine]): The data to initialize the dataset with.
            problem_type (ProblemType): The problem type.
            feature_columns (List[str]): The list of feature columns.
            feature_importance (dict): The feature importance.
            categorical_columns (List[str], optional): The list of categorical columns. Defaults to [].
            label_column (str, optional): The label column. Defaults to None.
            prediction_column (str, optional): The prediction column. Defaults to None.
            probability_column (str, optional): The probability column. Defaults to None.
            scoring_fn (callable, optional): The scoring function. Accepts a dataframe with features as columns and
                returns a tuple of numpy array of probabilities array of shape `(n_samples,n_classes)` and numpy
                array of prediction vector of shape `(n_samples,)`. Defaults to None.

        Raises:
            NotImplementedError: Needs to be implemented by child classes
        """
        raise NotImplementedError

    def set_control_box(self, advanced_controls: dict = {}) -> None:
        self.advanced_controls = advanced_controls

        control_box = ControlBoxManager().get_control_box()

        if control_box is None:
            control_box = ControlBox()
            ControlBoxManager().set_control_box(control_box)

        if advanced_controls is None:
            advanced_controls = {}

        control_box.set_config_map(advanced_controls)

    def split_probability_scores(self, transactions: pd.DataFrame) -> pd.DataFrame:

        feature_columns = [
            column.name for column in self.get_feature_columns()]

        if self.problem_type == ProblemType.REGRESSION:
            return transactions[feature_columns].copy()

        class_probability_columns = [PROBABILITY_COLUMN_TEMPLATE.substitute(
            prediction=label) for label in self.predicted_labels]
        new_transactions = transactions.dropna(
            subset=[self.probability_column])
        new_transactions.reset_index(drop=True, inplace=True)

        if not len(new_transactions):
            return pd.DataFrame([], columns=feature_columns + class_probability_columns)

        result_df = new_transactions[feature_columns].copy()

        is_probability_list = new_transactions[self.probability_column].apply(
            lambda x: isinstance(x, (list, np.ndarray))).all()
        is_probability_str = new_transactions[self.probability_column].apply(
            lambda x: isinstance(x, (str))).all()

        if not is_probability_list and not is_probability_str:
            raise ValueError(
                f"Column {self.probability_column} is not a list or a string. {new_transactions[self.probability_column].dtype}")

        if is_probability_str:
            result_df[class_probability_columns] = pd.DataFrame(
                new_transactions[self.probability_column].apply(
                    lambda x: json.loads(x)).values.tolist(),
                index=new_transactions.index)
        elif is_probability_list:
            result_df[class_probability_columns] = pd.DataFrame(
                new_transactions[self.probability_column].values.tolist(), index=new_transactions.index)

        return result_df

    @classmethod
    def convert_to_engine(cls, data: dict) -> sqlalchemy.engine.base.Engine:
        """Convert the data to a sqlalchemy engine.

        Args:
            data (dict): The data to convert to a sqlalchemy engine.

        Returns:
            sqlalchemy.engine.base.Engine: The sqlalchemy engine.
        """

        connection = Connection.from_dict(data)
        return connection.engine

    def validate_connection_properties(self, data: dict):
        if get(data, "storage_details.type") != "jdbc":
            raise ValueError(
                f"Unsupported connection type: {get(data, 'storage_details.type')}")

        if get(data, "storage_details.connection.location_type") not in ("db2", "postgresql"):
            raise ValueError(
                f"Unsupported database type: {get(data, 'storage_details.connection.location_type')}")

        if not get(data, "storage_details.connection.jdbc_url"):
            raise ValueError("jdbc_url is required")

        if not get(data, "tables"):
            raise ValueError("tables is required")

        tables_arr = get(data, "tables")

        if len(tables_arr) != 1:
            raise ValueError(
                f"Only one table is supported. Got {len(tables_arr)}")

        table_type = get(tables_arr[0], "type")
        if (self.type == DataSetType.BASELINE) and (table_type != "training"):
            raise ValueError(
                f"Table of type {table_type} not supported. Supported types 'training'.")
        elif (self.type == DataSetType.PRODUCTION) and (table_type != "payload"):
            raise ValueError(
                f"Table of type {table_type} not supported. Supported types 'payload'.")

        if not get(tables_arr[0], "database"):
            raise ValueError("database is required for drift operations.")

        if not get(tables_arr[0], "schema"):
            raise ValueError("schema is required for drift operations.")

        if not get(tables_arr[0], "table"):
            raise ValueError("table is required for drift operations.")

    def validate_data(self, **kwargs) -> None:
        start_time = DateTimeUtil.current_milli_time()

        if "data" not in kwargs:
            raise ValueError("'data' is mandatory.")
        data = kwargs["data"]

        supported_data = False
        if isinstance(data, pd.DataFrame):
            supported_data = True
        elif isinstance(data, dict):
            """
                The dictionary format
                {
                    "storage_details" : {
                        "type": "jdbc",
                        "connection": {
                            "location_type": "db2/postgresql",
                            "jdbc_url": "",
                            "jdbc_driver": "",
                            "use_ssl": "",
                            "certificate": ""
                        },
                        "credentials": {
                            "username": "",
                            "password": ""
                        }
                    },
                    "tables" : [{
                        "type": "training",
                        "database": "",
                        "schema": "",
                        "table": ""
                    }]
                }
            """

            supported_data = True
            self.validate_connection_properties(data)
            tables_arr = get(data, "tables")
            self.schema_name = get(tables_arr[0], "schema")
            self.table_name = get(tables_arr[0], "table")
            data = DriftDataSet.convert_to_engine(data)

        if not supported_data:
            raise ValueError(f"Data type {type(data)} is not supported")

        self.data_schema = self.get_data_schema(data)

        if "feature_columns" not in kwargs:
            raise ValueError("'feature_columns' is mandatory.")

        for column in kwargs["feature_columns"]:
            if not is_exists(column, self.data_schema):
                raise ValueError(
                    f"Feature Column {column} is not present in data")

        categorical_columns = get(kwargs, "categorical_columns", [])
        for column in categorical_columns:
            if not is_exists(column, self.data_schema):
                raise ValueError(
                    f"Categorical Column {column} is not present in data")

        label_column = get(kwargs, "label_column", None)
        if label_column is not None and not is_exists(label_column, self.data_schema):
            raise ValueError(
                f"Label Column {label_column} is not present in data")

        prediction_column = get(kwargs, "prediction_column", None)
        scoring_fn = get(kwargs, "scoring_fn", None)
        if (prediction_column is not None) and (
                scoring_fn is None) and not is_exists(prediction_column, self.data_schema):
            raise ValueError(
                f"Prediction Column {prediction_column} is not present in data")

        probability_column = get(kwargs, "probability_column", None)
        if (probability_column is not None) and (
                scoring_fn is None) and not is_exists(probability_column, self.data_schema):
            raise ValueError(
                f"Probability Column {probability_column} is not present in data")

        if scoring_fn is not None and not callable(scoring_fn):
            raise ValueError(f"Score Function {scoring_fn} is not callable")

        if (prediction_column is None) and (probability_column is None) and (scoring_fn is None):
            raise ValueError(
                "A scoring_fn should be provided if prediction_column or probability_column is not provided")

        # TODO Need to think of a solution here. For cases where, prediction/probability columns
        # are supplied, but scoring_fn is supplied, we need to validate that the prediction/probability
        # is indeed coming from the output.

        feature_importance = get(kwargs, "feature_importance", {})
        if (not isinstance(feature_importance, dict)):
            raise ValueError(
                f"Feature Importance {feature_importance} is not valid")

        record_id_column = get(kwargs, "record_id_column", None)
        if record_id_column is not None and not is_exists(record_id_column, self.data_schema):
            raise ValueError(
                f"Record ID Column {record_id_column} is not present in data")

        record_timestamp_column = get(kwargs, "record_timestamp_column", None)
        if record_timestamp_column is not None and not is_exists(record_timestamp_column, self.data_schema):
            raise ValueError(
                f"Record Timestamp Column {record_timestamp_column} is not present in data")

        start_timestamp = get(kwargs, "start_timestamp", None)
        if start_timestamp is not None:
            if not (isinstance(start_timestamp, datetime)):
                raise ValueError(
                    f"The start time {start_timestamp} is of incorrect type {type(start_timestamp)}. Should be 'datetime'.")
            if start_timestamp > datetime.now():
                raise ValueError(
                    f"The start time {start_timestamp} should not be in future.")

        end_timestamp = get(kwargs, "end_timestamp", None)
        if end_timestamp is not None:
            if not (isinstance(end_timestamp, datetime)):
                raise ValueError(
                    f"End Timestamp {end_timestamp} is of incorrect type {type(end_timestamp)}. Should be 'datetime'.")
            if end_timestamp > datetime.now():
                raise ValueError(
                    f"The end time {end_timestamp} should not be in future.")

        if start_timestamp is not None and end_timestamp is not None and start_timestamp >= end_timestamp:
            raise ValueError(
                f"The start time {start_timestamp} should be less than the end time {end_timestamp}.")

        min_samples = get(kwargs, "min_samples", None)
        max_samples = get(kwargs, "max_samples", None)

        if (min_samples is not None) and (max_samples is not None) and (min_samples > max_samples):
            raise ValueError(
                f"The min_samples '{min_samples}' provided is greater than the max_samples '{max_samples}' provided.")

        logger.log_info(
            "Validation completed.",
            **get_logging_params(
                data_set=self,
                start_time=start_time))

    @abstractmethod
    def get_data_schema(self,
                        data: Union[pd.DataFrame,
                                    sqlalchemy.engine.base.Engine]) -> Dict[str,
                                                                            str]:
        """Get the data schema.

        Args:
            data (Union[pd.DataFrame, sqlalchemy.engine.base.Engine]): The data to get the schema from.

        Returns:
            Dict[str, str]: The schema of the table. The keys are the column names
                and the values are the column types
        """
        raise NotImplementedError

    def add_column(self, column: DataColumn) -> None:
        """Add a column to the dataset.

        Args:
            column (DataColumn): The column to add.

        Raises:
            ValueError: If the column already exists.
        """
        if column.name in self.columns:
            raise ValueError(
                f"Column {column.name} already exists in the dataset.")

        column.set_data_set(self)
        self.columns[column.name] = column

    def get_column(self, column_name: str) -> DataColumn:
        """Get a column by name.

        Args:
            column_name (str): The name of the column to get.

        Raises:
            ValueError: If the column does not exist in the dataset.

        Returns:
            DataColumn: The column.
        """
        if column_name not in self.columns:
            raise ValueError(f"Column {column_name} not found in the dataset.")

        return self.columns[column_name]

    def get_label_column(self) -> DataColumn:
        """Get the label column.

        Raises:
            ValueError: If the label column is not found.

        Returns:
            DataColumn: The label column.
        """
        for column in self.columns.values():
            if column.role == ColumnRole.LABEL:
                return column

        raise ValueError("Label column not found")

    def get_prediction_column(self) -> DataColumn:
        """Get the prediction column.

        Raises:
            ValueError: If the prediction column is not found.

        Returns:
            DataColumn: The prediction column.
        """
        for column in self.columns.values():
            if column.role == ColumnRole.PREDICTION:
                return column

        raise ValueError("Prediction column not found")

    def get_feature_columns(self) -> List[DataColumn]:
        """Get the list of feature columns.

        Returns:
            List[DataColumn]: The list of feature columns
        """
        return [
            column for column in self.columns.values() if column.role in (
                ColumnRole.FEATURE,
                ColumnRole.CATEGORICAL)]

    def get_categorical_columns(self) -> List[DataColumn]:
        """Get the list of categorical columns.

        Returns:
            List[DataColumn]: The list of categorical columns
        """
        return [column for column in self.columns.values() if column.role == ColumnRole.CATEGORICAL]

    def get_probability_score_columns(self) -> List[DataColumn]:
        """Get the list of probability score columns.

        Returns:
            List[DataColumn]: The list of probability score columns
        """
        return [column for column in self.columns.values() if column.role ==
                ColumnRole.PROBABILITY_SCORE]

    def get_operation_columns(self) -> List[DataColumn]:
        """Get the list of columns for single feature operations.

        Returns:
            List[DataColumn]: The list of columns for single feature operations.
        """
        return [column for column in self.columns.values() if column.is_eligible_for_operation]

    def get_data_quality_issue_columns(self, kind: DataQualityIssueKind) -> List[DataColumn]:
        """Get the list of columns for data quality issues.

        Returns:
            List[DataColumn]: The list of columns for single feature operations.
        """

        columns = []

        if kind == DataQualityIssueKind.MISSING_VALUE:
            # All numerical and categorical columns that are eligible for data quality
            # and operation computation.
            columns = [column for column in self.columns.values() if column.role in (
                ColumnRole.CATEGORICAL, ColumnRole.FEATURE) and column.is_eligible_for_data_quality
                and column.is_eligible_for_operation]

        elif kind in (DataQualityIssueKind.CATEGORICAL_OUTLIER, DataQualityIssueKind.EMPTY_STRING):
            # All categorical columns that are eligible for data quality and operation computation.
            columns = [column for column in self.columns.values() if (column.role == ColumnRole.CATEGORICAL)
                       and column.is_eligible_for_operation and column.is_eligible_for_data_quality]

        if kind == DataQualityIssueKind.NUMERICAL_IQR_OUTLIER:
            # All numerical feature columns that are not discrete and are eligible for
            # data quality and operation computation.
            columns = [
                column for column in self.columns.values() if (
                    column.role == ColumnRole.FEATURE) and column.is_eligible_for_operation and column.is_eligible_for_data_quality and (
                    not column.is_discrete)]

        return columns

    def get_insights_columns(
            self, source_column: DataColumn = None) -> List[Tuple[DataColumn, DataColumn]]:
        """Get the list of columns for insights.

        Returns:
            List[Tuple[DataColumn, DataColumn]]: The list of columns for insights
        """
        eligible_columns = [
            column for column in self.columns.values() if column.is_eligible_for_insights]

        source_columns = []
        if source_column is not None:
            source_columns.append(source_column)
        else:
            source_columns += [
                column for column in eligible_columns if isinstance(
                    column, CategoricalColumn)]
            source_columns += [
                column for column in eligible_columns if isinstance(
                    column, NumericalColumn) and column.is_discrete]

            source_columns = sorted(source_columns, reverse=True)
        target_columns = [
            column for column in eligible_columns if isinstance(
                column, (CategoricalColumn, NumericalColumn))]
        insight_columns = []
        for (source, target) in product(source_columns, target_columns):
            if source.name == target.name:
                continue

            if (target, source) in insight_columns:
                continue

            insight_columns.append((source, target))

        return insight_columns

    def delete_column(self, column_name: str) -> None:
        """Delete a column from the dataset.

        Args:
            column_name (str): The name of the column to delete.

        Raises:
            ValueError: If the column does not exist in the dataset.
        """
        if column_name not in self.columns:
            raise ValueError(f"Column {column_name} not found")

        del self.columns[column_name]

    def add_operation(self, operation: Operation) -> None:
        """Add an operation to the dataset.

        Args:
            operation (Operation): The operation to add.

        Raises:
            ValueError: If the operation already exists in the dataset.
        """

        if operation.name in self.operations:
            raise ValueError(
                f"Operation {operation.name} already exists in the dataset.")

        operation.set_data_set(self)
        for statistics in operation.statistics.values():
            statistics.set_data_set(self)
        self.operations[operation.name] = operation

    def add_data_quality_issue(self, issue: DataQualityIssue) -> None:
        """Add a data quality issue to the dataset.

        Args:
            issue (DataQualityIssue): The issue to add.

        Raises:
            ValueError: If the issue already exists in the dataset.
        """
        if issue.name in self.data_quality_issues:
            raise ValueError(
                f"Data Quality Issue {issue.name} already exists in the dataset.")

        self.data_quality_issues[issue.name] = issue

    def get_data_quality_issue(self, issue_kind: DataQualityIssueKind,
                               column: DataColumn) -> DataQualityIssue:
        dq_name = f"{issue_kind.value}_{column.name}"

        if dq_name not in self.data_quality_issues:
            raise ValueError(
                f"Data Quality issue {dq_name} not found in the dataset.")
        return self.data_quality_issues[dq_name]

    async def add_data_quality_issues(self,
                                      data: Union[pd.DataFrame,
                                                  sqlalchemy.engine.base.Engine]) -> None:

        issue_coros = []
        for issue_kind in DataQualityIssueKind:
            for column in self.get_data_quality_issue_columns(kind=issue_kind):
                issue = DataQualityIssue.factory(issue_kind=issue_kind)
                operation = self.get_single_operations(
                    target_columns=[column])[0]
                issue_coros.append(
                    issue.learn(
                        target_column=column,
                        operation=operation,
                        data_set=self,
                        data=data))

        issues = await gather_with_concurrency(*issue_coros)
        for issue in issues:
            self.add_data_quality_issue(issue)

    async def add_single_operations(self,
                                    data: Union[pd.DataFrame,
                                                sqlalchemy.engine.base.Engine]) -> None:
        operation_coros = []
        for target_column in self.get_operation_columns():
            operation = Operation.factory(target_column=target_column)
            self.add_operation(operation)
            operation_coros.append(operation.execute(data))

        await gather_with_concurrency(*operation_coros)

    async def add_two_column_operations(self,
                                        data: Union[pd.DataFrame,
                                                    sqlalchemy.engine.base.Engine]) -> None:
        operation_coros = []
        for source_column, target_column in self.get_insights_columns():
            operation = Operation.factory(
                target_column=target_column, source_column=source_column)
            self.add_operation(operation)

            source_statistics = self.get_statistics(
                target_column=source_column)
            operation_coros.append(operation.execute(
                data, source_statistics=source_statistics))

        await gather_with_concurrency(*operation_coros)

    def get_single_operations(self, target_columns: List[DataColumn] = []) -> List[Operation]:
        """Get the list of single column operations

        Returns:
            List[Operation]: The list of single column operations
        """
        def filter_fn(op):
            condition = op.kind in (
                OperationKind.CONTINUOUS_FEATURE_COUNTS,
                OperationKind.DISCRETE_FEATURE_COUNTS)

            if target_columns and len(target_columns):
                names = [column.name for column in target_columns]
                condition = condition and (op.target_column.name in names)

            return condition

        x = list(filter(filter_fn, self.operations.values()))

        if len(x) == 0:
            logger.log_warning(f"No operations found.")
        return x

    def get_all_statistics(self,
                           column: DataColumn,
                           value: Union[str,
                                        Tuple]) -> Dict[str,
                                                        Statistics]:
        """Get a dictionary of statistics which are computed on the given column and value.

        Args:
            column (DataColumn): The column object
            value (Union[str, Tuple]): The value to look for.
            1. If the column is Categorical, the value is a string
            2. If the column is Numerical, the value is a tuple representing the range with (lower bound, upper bound)

        Returns:
            Dict[str, Statistics]: The dictionary of statistics. The statistics id is the key.
        """
        all_statistics = {}

        for operation in self.operations.values():
            if operation.kind == OperationKind.DISCRETE_DISCRETE_FEATURE_COUNTS:
                if operation.source_column.name == column.name:
                    all_statistics.update(
                        {dist.name: dist for dist in operation.statistics.values() if dist.source_value == value})
                elif operation.target_column.name == column.name:
                    source_statistics = self.get_statistics(
                        target_column=column)
                    mirrored_statistics = operation.create_statistics(
                        value, source_statistics=source_statistics)
                    all_statistics.update(
                        {mirrored_statistics.name: mirrored_statistics})
            elif operation.kind == OperationKind.DISCRETE_CONTINUOUS_FEATURE_COUNTS:
                if operation.source_column.name == column.name:
                    all_statistics.update(
                        {dist.name: dist for dist in operation.statistics.values() if dist.source_value == value})
                elif operation.target_column.name == column.name:
                    new_statistics = operation.create_statistics(value)
                    all_statistics.update(
                        {new_statistics.name: new_statistics})

        return all_statistics

    def get_statistics(self,
                       target_column: DataColumn,
                       source_column: DataColumn = None,
                       source_value: str = None) -> Statistics:

        logger.log_debug("Getting statistics for column combination.",
                         **get_logging_params(source_column=source_column,
                                              target_column=target_column,
                                              source_value=source_value))
        if source_column is None and source_value is None:
            for operation in self.get_single_operations(target_columns=[target_column]):
                if operation.target_column == target_column:
                    return list(operation.statistics.values())[0]

        for operation in self.operations.values():
            if operation.target_column != target_column:
                continue

            if operation.source_column != source_column:
                continue

            for statistics in operation.statistics.values():
                if statistics.source_value == source_value:
                    return statistics

        return

    def get_data_quality_violations(
            self,
            issue_kind: DataQualityIssueKind,
            column: DataColumn) -> int:
        try:
            return get(self.data_quality_violations, f"{issue_kind.value}.{column.name}", 0)
        except AttributeError:
            return 0

    def convert_column_dtypes_to_native(self, dtype):
        """Convert the column dtypes (pandas) to native types.

        Args:
            dtype (_type_): The dtype to convert.

        Raises:
            ValueError: If the dtype is not supported.

        Returns:
            _type_: The native type
        """
        if dtype == "object":
            return "str"

        if dtype == "bool":
            return "bool"
        if np.issubdtype(dtype, np.integer):
            return "int"
        if np.issubdtype(dtype, np.floating):
            return "float"

        if "datetime" in dtype:
            return "datetime"

        raise ValueError(f"Unsupported data type {dtype}.")

    def set_feature_importance(self, feature_importance: dict) -> None:
        if all(isinstance(value, dict) for value in feature_importance.values()):
            # For multi class problems, the feature importance value could be a dict of dicts
            # { class -> { feature -> weight }}. In such cases, the final feature importance
            # will be aggregated across classes.
            new_feature_importance = {}
            for value in feature_importance.values():
                for feature, weight in value.items():
                    if feature not in new_feature_importance:
                        new_feature_importance[feature] = weight
                    else:
                        new_feature_importance[feature] += weight

            feature_importance = {**new_feature_importance}

        total = sum(feature_importance.values())

        # Normalize and sort the feature importance in decreasing order of weight
        self.feature_importance = {
            key: value / total for key,
            value in sorted(
                feature_importance.items(),
                key=lambda x: x[1],
                reverse=True)}

    def to_dict(self) -> dict:
        """Convert the dataset to a dictionary.

        Returns:
            dict: The dataset as a dictionary.
        """
        dict_ = {
            "id": self.id,
            "version": self.version,
            "type": self.type.value,
            "advanced_controls": self.advanced_controls,
            "count": get_python_types(self.count),
            "problem_type": self.problem_type.value,
            "schema": self.data_schema,
            "feature_importance": get_python_types(self.feature_importance)
        }

        if len(self.unique_labels):
            dict_["unique_labels"] = get_python_types(self.unique_labels)

        if len(self.predicted_labels):
            dict_["predicted_labels"] = get_python_types(self.predicted_labels)

        if self.probability_column is not None:
            dict_["probability_column"] = get_python_types(
                self.probability_column)

        if self.max_samples is not None:
            dict_["max_samples"] = get_python_types(self.max_samples)

        dict_["columns"] = {column.name: column.to_dict()
                            for column in self.columns.values()}
        dict_["operations"] = [operation.to_summary_dict()
                               for operation in self.operations.values()]

        dict_["data_quality_issues"] = [issue.to_summary_dict()
                                        for issue in self.data_quality_issues.values()]

        dict_["has_model_quality_drift"] = self.has_model_quality_drift
        dict_["has_data_quality_issues"] = self.has_data_quality_issues

        return dict_

    @classmethod
    def from_dict(cls, data: dict) -> "DriftDataSet":
        """Create a dataset from a dictionary.

        Args:
            data (dict): The dictionary to create the dataset from.

        Returns:
            DriftDataSet: The dataset.
        """

        try:
            if not ("summary.json" in data):
                raise ValueError(
                    "summary.json not found in the drift archive.")

            summary_dict = data["summary.json"]

            dataset = cls(DataSetType(summary_dict["type"]))
            dataset.id = summary_dict["id"]
            dataset.version = summary_dict["version"]
            dataset.advanced_controls = summary_dict["advanced_controls"]
            dataset.count = summary_dict["count"]
            dataset.problem_type = ProblemType(summary_dict["problem_type"])
            dataset.data_schema = summary_dict["schema"]
            dataset.feature_importance = summary_dict["feature_importance"]
            dataset.has_model_quality_drift = summary_dict["has_model_quality_drift"]
            dataset.has_data_quality_issues = summary_dict["has_data_quality_issues"]

            if "max_samples" in summary_dict:
                dataset.max_samples = summary_dict["max_samples"]

            if dataset.problem_type in (ProblemType.BINARY, ProblemType.MULTICLASS):
                dataset.unique_labels = summary_dict["unique_labels"]
                dataset.predicted_labels = summary_dict["predicted_labels"]
                dataset.probability_column = summary_dict["probability_column"]

                if "accuracy/meta_model.json" in data:
                    from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.meta_model import \
                        MetaModel
                    model_dict = data["accuracy/meta_model.json"]
                    dataset.meta_model = MetaModel.from_dict(model_dict)

                    if "accuracy/meta_model_object.pkl" in data:
                        dataset.meta_model.load(
                            model_object=data["accuracy/meta_model_object.pkl"])

            if "dialect" in summary_dict:
                dataset.dialect = summary_dict["dialect"]

            for column_dict_ in summary_dict["columns"].values():
                dataset.add_column(DataColumn.from_dict(column_dict_))

            for operation_summary in summary_dict["operations"]:
                start_time = DateTimeUtil.current_milli_time()
                key = f"operations/{operation_summary['kind']}/{operation_summary['file_name']}"
                operation_dict = data[key]
                target_column = dataset.get_column(
                    operation_summary["target_column"])
                operation = Operation.from_dict(operation_dict)
                operation.target_column = target_column

                if "source_column" in operation_summary:
                    source_column = dataset.get_column(
                        operation_summary["source_column"])
                    operation.source_column = source_column

                dataset.add_operation(operation)
                logger.log_info(
                    "Operation added to the dataset.",
                    **get_logging_params(
                        operation=operation,
                        start_time=start_time))

            for issue_summary in summary_dict["data_quality_issues"]:
                start_time = DateTimeUtil.current_milli_time()
                key = f"data_quality_issues/{issue_summary['kind']}/{issue_summary['file_name']}"
                data_quality_issue = DataQualityIssue.from_dict(data[key])
                dataset.add_data_quality_issue(data_quality_issue)
                logger.log_info(
                    "Data Quality Issue added to the dataset.",
                    **get_logging_params(start_time=start_time))

            if summary_dict["type"] == DataSetType.PRODUCTION.value:
                # TODO Figure out a way to do this from PayloadDataSet module instead.
                dataset.baseline_data_set_id = summary_dict["baseline_data_set_id"]
                dataset.record_id_column = get(
                    summary_dict, "record_id_column")
                dataset.record_timestamp_column = get(
                    summary_dict, "record_timestamp_column")
                dataset.data_quality_violations = get(
                    summary_dict, "data_quality_violations")
                dataset.start_timestamp = None
                dataset.end_timestamp = None

                if "start_timestamp" in summary_dict:
                    dataset.start_timestamp = datetime.fromisoformat(
                        summary_dict["start_timestamp"])

                if "end_timestamp" in summary_dict:
                    dataset.end_timestamp = datetime.fromisoformat(
                        summary_dict["end_timestamp"])

            return dataset
        except KeyError as e:
            raise ValueError(
                f"Cannot create a dataset from the given dictionary. Missing key {e}.") from e
        except pickle.PicklingError as pe:
            raise Exception(f"Can not load the meta model.") from pe
