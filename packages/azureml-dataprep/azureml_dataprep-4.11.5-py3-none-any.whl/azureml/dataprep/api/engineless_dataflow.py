# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import List, Dict, Any, Union
import os

import yaml

from azureml.dataprep.rslex import PyRsDataflow

from .engineapi.typedefinitions import (InspectorArguments, ExecuteInspectorCommonResponse)
from .dataprofile import DataProfile
from .inspector import BaseInspector
from .step import Step
from ._dataframereader import RecordIterable, _execute, get_dataframe_reader
from ._partitionsreader import PartitionIterable
from .dataflow import Dataflow
from ._loggerfactory import _LoggerFactory, track, trace
from .tracing._open_telemetry_adapter import to_dprep_span_context


logger = None
tracer = trace.get_tracer(__name__)

def get_logger():
    global logger
    if logger is not None:
        return logger

    logger = _LoggerFactory.get_logger("Dataflow")
    return logger


class EnginelessDataflow(Dataflow):
    """
    Dataflow wrapper around a RSlex Dataflow YAML. Does not support the addition of any transformation steps
    Clex engine activity, etc.
    """

    def __init__(self, py_rs_dataflow):
        # fake attribute to trick AbstractDataset._should_auto_inference with AbstractDatset._load
        Dataflow.__init__(self, engine_api=None)
        self.meta = {'infer_column_types': 'False'}

        if isinstance(py_rs_dataflow, str):
            from azureml.dataprep.api._rslex_executor import ensure_rslex_environment
            ensure_rslex_environment()
            # covers validation
            self._py_rs_dataflow = PyRsDataflow(py_rs_dataflow)
        elif isinstance(py_rs_dataflow, PyRsDataflow):
            self._py_rs_dataflow = py_rs_dataflow
        else:
            raise ValueError('Expect RSlex Dataflow YAML string or RSlex PyRsDataflow')

    def __repr__(self) -> str:
        return 'EnginelessDataflow:\n' + self._py_rs_dataflow.to_yaml_string()

    def _to_yaml_dict(self) -> dict:
        return yaml.safe_load(self._py_rs_dataflow.to_yaml_string())

    def _copy_and_update_metadata(self,
                                  action: str,
                                  source: str,
                                  **kwargs) -> 'Dataflow':
        # py_rs_dataflow is immutable so even if no changes occur & same instance is passed, nothing bad should happen
        new_py_rs_dataflow = self._py_rs_dataflow

        if not new_py_rs_dataflow.has_schema_property('metadata', 'activity'):
            new_py_rs_dataflow = new_py_rs_dataflow.set_schema_property('metadata', 'activity', action)

        if not new_py_rs_dataflow.has_schema_property('metadata', 'activityApp'):
            new_py_rs_dataflow = new_py_rs_dataflow.set_schema_property('metadata', 'activityApp', source)

        run_id = os.environ.get("AZUREML_RUN_ID", None)
        if run_id is not None:
            # keep this here so not to break existing reporting
            new_py_rs_dataflow = new_py_rs_dataflow.set_schema_property('metadata', 'runId', run_id)
            new_py_rs_dataflow = new_py_rs_dataflow.set_schema_property('metadata', 'run_id', run_id)

        for (k, v) in kwargs.items():
            if not new_py_rs_dataflow.has_schema_property('metadata', k):
                new_py_rs_dataflow = new_py_rs_dataflow.set_schema_property('metadata', k, v)

        return EnginelessDataflow(new_py_rs_dataflow)

    def add_step(self,
                 step_type: str,
                 arguments: Dict[str, Any],
                 local_data: Dict[str, Any] = None) -> 'Dataflow':
        raise NotImplementedError

    def _add_transformation(self, step, args):
        return EnginelessDataflow(self._py_rs_dataflow.add_transformation(step, args, None))

    def take(self, count: int) -> 'Dataflow':
        """
        Takes the specified count of records.

        :param count: The number of records to take.
        :return: The modified Dataflow.
        """
        if not (isinstance(count, int) and count > 0):
            raise ValueError('count must be a positive integer')
        return self._add_transformation('take', count)

    def _with_partition_size(self, partition_size: int) -> 'Dataflow':
        if not (isinstance(partition_size, int) and partition_size > 0):
            raise ValueError('expect partition_size to be positive int')

        rs_dataflow_yaml = self._to_yaml_dict()
        transformations = rs_dataflow_yaml['transformations'][0]
        # invalid parition size test, json lines paritiont size test
        if 'read_delimited' in transformations:
            transformation = transformations['read_delimited']
        elif 'read_json_lines' in transformations:
            transformation = transformations['read_json_lines']
        else:
            raise ValueError('Can only update partition_size if `read_delimited` or `read_json_lines` '
                             'are in the EnglinelessDataflow')

        transformation['partition_size'] = partition_size
        rs_dataflow_str = yaml.safe_dump(rs_dataflow_yaml)
        return EnginelessDataflow(rs_dataflow_str)

    def _get_steps(self) -> List[Step]:
        raise NotImplementedError

    def execute_inspector(self, inspector: BaseInspector) -> ExecuteInspectorCommonResponse:
        raise NotImplementedError

    def _execute_inspector(self, inspector: Union[str, InspectorArguments]) -> ExecuteInspectorCommonResponse:
        raise NotImplementedError

    def execute_inspectors(self, inspectors: List[BaseInspector]) \
            -> Dict[InspectorArguments, ExecuteInspectorCommonResponse]:
        raise NotImplementedError

    def _execute_inspectors(self, inspectors: Union[str, List[InspectorArguments]]) \
            -> Dict[InspectorArguments, ExecuteInspectorCommonResponse]:
        raise NotImplementedError

    def _get_profile(self,
                     include_stype_counts: bool = False,
                     number_of_histogram_bins: int = 10,
                     include_average_spaces_count: bool = False,
                     include_string_lengths: bool = False) -> DataProfile:
        raise NotImplementedError

    @track(get_logger)
    def get_partition_count(self) -> int:
        from azureml.dataprep.api._dataframereader import get_partition_count_with_rslex
        return get_partition_count_with_rslex(self._py_rs_dataflow.to_yaml_string())

    @track(get_logger)
    def run_local(self) -> None:
        """
        Runs the current Dataflow using the local execution runtime.
        """
        parent = trace.get_current_span()
        with tracer.start_as_current_span('Dataflow.run_local', parent) as span:
            _execute('Dataflow.run_local',
                     self._py_rs_dataflow.to_yaml_string(),
                     force_clex=False,
                     allow_fallback_to_clex=False,
                     span_context=to_dprep_span_context(span.get_context()))

    @track(get_logger)
    def run_spark(self) -> None:
        raise NotImplementedError

    @track(get_logger)
    def _to_pyrecords(self):
        raise NotImplementedError

    def select_partitions(self, partition_indices: List[int]) -> 'Dataflow':
        """
        Selects specific partitions from the data, dropping the rest.

        :return: The modified Dataflow.
        """
        return self._add_transformation('select_partitions', partition_indices)

    def _partition_to_pandas_dataframe(self,
                                       i: int,
                                       extended_types: bool,
                                       nulls_as_nan: bool,
                                       on_error: str,
                                       out_of_range_datetime: str) -> 'pandas.DataFrame':
        return self.select_partitions([i]).to_pandas_dataframe(extended_types=extended_types,
                                                               nulls_as_nan=nulls_as_nan,
                                                               on_error=on_error,
                                                               out_of_range_datetime=out_of_range_datetime)

    @track(get_logger)
    def to_dask_dataframe(self,
                          sample_size: int = 10000,
                          dtypes: dict = None,
                          extended_types: bool = False,
                          nulls_as_nan: bool = True,
                          on_error: str = 'null',
                          out_of_range_datetime: str = 'null'):
        """
        Returns a Dask DataFrame that can lazily read the data in the Dataflow.

        .. remarks::
            Dask DataFrames allow for parallel and lazy processing of data by splitting the data into multiple
                partitions. Because Dask DataFrames don't actually read any data until a computation is requested,
                it is necessary to determine what the schema and types of the data will be ahead of time. This is done
                by reading a specific number of records from the Dataflow (specified by the `sample_size` parameter).
                However, it is possible for these initial records to have incomplete information. In those cases, it is
                possible to explicitly specify the expected columns and their types by providing a dict of the shape
                `{column_name: dtype}` in the `dtypes` parameter.

        :param sample_size: The number of records to read to determine schema and types.
        :param dtypes: An optional dict specifying the expected columns and their dtypes.
            `sample_size` is ignored if this is provided.
        :param extended_types: Whether to keep extended DataPrep types such as DataPrepError in the DataFrame. If False,
            these values will be replaced with None.
        :param nulls_as_nan: Whether to interpret nulls (or missing values) in number typed columns as NaN. This is
            done by pandas for performance reasons; it can result in a loss of fidelity in the data.
        :param on_error: How to handle any error values in the Dataflow, such as those produced by an error while parsing values.
            Valid values are 'null' which replaces them with null; and 'fail' which will result in an exception.
        :param out_of_range_datetime: How to handle date-time values that are outside the range supported by Pandas.
            Valid values are 'null' which replaces them with null; and 'fail' which will result in an exception.
        :return: A Dask DataFrame.
        """
        from ._dask_helper import have_dask, DaskImportError
        from ._pandas_helper import have_pandas

        if not (have_dask() and have_pandas()):
            raise DaskImportError()

        import dask.dataframe as dd
        from dask.delayed import delayed
        import pandas

        # TODO defaulting to non-optimized dask, optimized dask in future PR (nathof)
        partition_count = self.get_partition_count()

        if partition_count <= 0:
            return dd.from_pandas(pandas.DataFrame(), chunksize=1)

        dtypes = dtypes or {col: str(t) for (col, t) in self.take(sample_size).to_pandas_dataframe().dtypes.items()}
        delayed_functions = [delayed(self._partition_to_pandas_dataframe)(i, extended_types, nulls_as_nan, on_error, out_of_range_datetime) for i in range(0, partition_count)]
        return dd.from_delayed(delayed_functions, meta=dtypes)

    @track(get_logger)
    def to_spark_dataframe(self, spark_session: 'pyspark.sql.SparkSession' = None) -> 'pyspark.sql.DataFrame':
        raise NotImplementedError

    @track(get_logger)
    def to_record_iterator(self) -> RecordIterable:
        raise NotImplementedError

    @track(get_logger)
    def to_partition_iterator(self, on_error: str = 'null') -> PartitionIterable:
        raise NotImplementedError

    # noinspection PyUnresolvedReferences
    @track(get_logger)
    def to_pandas_dataframe(self,
                            extended_types: bool = False,
                            nulls_as_nan: bool = True,
                            on_error: str = 'null',
                            out_of_range_datetime: str = 'null') -> 'pandas.DataFrame':
        """
        Pulls all of the data and returns it as a Pandas `Link pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_.

        .. remarks::

            This method will load all the data returned by this Dataflow into memory.

            Since Dataflows do not require a fixed, tabular schema but Pandas DataFrames do, an implicit tabularization
                step will be executed as part of this action. The resulting schema will be the union of the schemas of all
                records produced by this Dataflow.

        :param extended_types: Whether to keep extended DataPrep types such as DataPrepError in the DataFrame. If False,
            these values will be replaced with None.
        :param nulls_as_nan: Whether to interpret nulls (or missing values) in number typed columns as NaN. This is
            done by pandas for performance reasons; it can result in a loss of fidelity in the data.
        :param on_error: How to handle any error values in the Dataflow, such as those produced by an error while parsing values.
            Valid values are 'null' which replaces them with null; and 'fail' which will result in an exception.
        :param out_of_range_datetime: How to handle date-time values that are outside the range supported by Pandas.
            Valid values are 'null' which replaces them with null; and 'fail' which will result in an exception.
        :return: A Pandas `Link pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_.
        """
        with tracer.start_as_current_span('Dataflow.to_pandas_dataframe', trace.get_current_span()) as span:
            span_context = to_dprep_span_context(span.get_context())
            return get_dataframe_reader().to_pandas_dataframe(self._py_rs_dataflow.to_yaml_string(),
                                                              extended_types,
                                                              nulls_as_nan,
                                                              on_error,
                                                              out_of_range_datetime,
                                                              span_context)
