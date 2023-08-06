from typing import List
from typing import Optional

from mlopsdna.evidently.base_metric import InputData
from mlopsdna.evidently.metric_preset.metric_preset import MetricPreset
from mlopsdna.evidently.metrics import RegressionAbsPercentageErrorPlot
from mlopsdna.evidently.metrics import RegressionErrorBiasTable
from mlopsdna.evidently.metrics import RegressionErrorDistribution
from mlopsdna.evidently.metrics import RegressionErrorNormality
from mlopsdna.evidently.metrics import RegressionErrorPlot
from mlopsdna.evidently.metrics import RegressionPredictedVsActualPlot
from mlopsdna.evidently.metrics import RegressionPredictedVsActualScatter
from mlopsdna.evidently.metrics import RegressionQualityMetric
from mlopsdna.evidently.metrics import RegressionTopErrorMetric
from mlopsdna.evidently.utils.data_operations import DatasetColumns


class RegressionPreset(MetricPreset):
    """Metric preset for Regression performance analysis.

    Contains metrics:
    - RegressionQualityMetric
    - RegressionPredictedVsActualScatter
    - RegressionPredictedVsActualPlot
    - RegressionErrorPlot
    - RegressionAbsPercentageErrorPlot
    - RegressionErrorDistribution
    - RegressionErrorNormality
    - RegressionTopErrorMetric
    - RegressionErrorBiasTable
    """

    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        super().__init__()
        self.columns = columns

    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [
            RegressionQualityMetric(),
            RegressionPredictedVsActualScatter(),
            RegressionPredictedVsActualPlot(),
            RegressionErrorPlot(),
            RegressionAbsPercentageErrorPlot(),
            RegressionErrorDistribution(),
            RegressionErrorNormality(),
            RegressionTopErrorMetric(),
            RegressionErrorBiasTable(columns=self.columns),
        ]
