from typing import List
from typing import Optional

from mlopsdna.evidently.base_metric import InputData
from mlopsdna.evidently.calculations.classification_performance import get_prediction_data
from mlopsdna.evidently.metric_preset.metric_preset import MetricPreset
from mlopsdna.evidently.metrics import ClassificationClassBalance
from mlopsdna.evidently.metrics import ClassificationClassSeparationPlot
from mlopsdna.evidently.metrics import ClassificationConfusionMatrix
from mlopsdna.evidently.metrics import ClassificationPRCurve
from mlopsdna.evidently.metrics import ClassificationProbDistribution
from mlopsdna.evidently.metrics import ClassificationPRTable
from mlopsdna.evidently.metrics import ClassificationQualityByClass
from mlopsdna.evidently.metrics import ClassificationQualityByFeatureTable
from mlopsdna.evidently.metrics import ClassificationQualityMetric
from mlopsdna.evidently.metrics import ClassificationRocCurve
from mlopsdna.evidently.utils.data_operations import DatasetColumns


class ClassificationPreset(MetricPreset):
    """
    Metrics preset for classification performance.

    Contains metrics:
    - ClassificationQualityMetric
    - ClassificationClassBalance
    - ClassificationConfusionMatrix
    - ClassificationQualityByClass
    """

    columns: Optional[List[str]]
    probas_threshold: Optional[float]
    k: Optional[int]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
    ):
        super().__init__()
        self.columns = columns
        self.probas_threshold = probas_threshold
        self.k = k

    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        result = [
            ClassificationQualityMetric(probas_threshold=self.probas_threshold, k=self.k),
            ClassificationClassBalance(),
            ClassificationConfusionMatrix(probas_threshold=self.probas_threshold, k=self.k),
            ClassificationQualityByClass(probas_threshold=self.probas_threshold, k=self.k),
        ]
        curr_predictions = get_prediction_data(data.current_data, columns, data.column_mapping.pos_label)

        if curr_predictions.prediction_probas is not None:
            result.extend(
                [
                    ClassificationClassSeparationPlot(),
                    ClassificationProbDistribution(),
                    ClassificationRocCurve(),
                    ClassificationPRCurve(),
                    ClassificationPRTable(),
                ]
            )

        result.append(ClassificationQualityByFeatureTable(columns=self.columns))
        return result
