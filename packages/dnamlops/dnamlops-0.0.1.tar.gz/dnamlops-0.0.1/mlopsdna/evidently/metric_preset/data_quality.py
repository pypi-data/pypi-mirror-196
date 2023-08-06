from typing import List
from typing import Optional

from mlopsdna.evidently.base_metric import InputData
from mlopsdna.evidently.metric_preset.metric_preset import MetricPreset
from mlopsdna.evidently.metrics import ColumnSummaryMetric
from mlopsdna.evidently.metrics import DatasetCorrelationsMetric
from mlopsdna.evidently.metrics import DatasetSummaryMetric
from mlopsdna.evidently.metrics.base_metric import generate_column_metrics
from mlopsdna.evidently.metrics.data_integrity.dataset_missing_values_metric import DatasetMissingValuesMetric
from mlopsdna.evidently.utils.data_operations import DatasetColumns


class DataQualityPreset(MetricPreset):
    """Metric preset for Data Quality analysis.

    Contains metrics:
    - DatasetSummaryMetric
    - ColumnSummaryMetric for each column
    - DatasetMissingValuesMetric
    - DatasetCorrelationsMetric

    Args:
        columns: list of columns for analysis.
    """

    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        super().__init__()
        self.columns = columns

    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [
            DatasetSummaryMetric(),
            generate_column_metrics(ColumnSummaryMetric, columns=self.columns, skip_id_column=True),
            DatasetMissingValuesMetric(),
            DatasetCorrelationsMetric(),
        ]
