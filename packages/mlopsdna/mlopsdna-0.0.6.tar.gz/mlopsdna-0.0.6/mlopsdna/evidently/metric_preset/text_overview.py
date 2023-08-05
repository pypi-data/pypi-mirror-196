from typing import Dict
from typing import Optional

from mlopsdna.evidently.base_metric import InputData
from mlopsdna.evidently.features.generated_features import FeatureDescriptor
from mlopsdna.evidently.metric_preset.metric_preset import MetricPreset
from mlopsdna.evidently.metrics import ColumnDriftMetric
from mlopsdna.evidently.metrics import ColumnSummaryMetric
from mlopsdna.evidently.metrics import TextDescriptorsCorrelationMetric
from mlopsdna.evidently.metrics import TextDescriptorsDistribution
from mlopsdna.evidently.metrics import TextDescriptorsDriftMetric
from mlopsdna.evidently.utils.data_operations import DatasetColumns


class TextOverviewPreset(MetricPreset):
    """Metric preset for text column analysis.

    Contains metrics:
    - ColumnSummaryMetric
    - TextDescriptorsDistribution
    - TextDescriptorsCorrelation
    - ColumnDriftMetric
    - TextDescriptorsDescriptorsDriftMetric

    Args:
        column_name: text column name.
    """

    column_name: str

    def __init__(self, column_name: str, descriptors: Optional[Dict[str, FeatureDescriptor]] = None):
        super().__init__()
        self.column_name = column_name
        self.descriptors = descriptors

    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        result = [
            ColumnSummaryMetric(column_name=self.column_name),
            TextDescriptorsDistribution(column_name=self.column_name, descriptors=self.descriptors),
            TextDescriptorsCorrelationMetric(column_name=self.column_name, descriptors=self.descriptors),
        ]
        if data.reference_data is not None:
            result.extend(
                [
                    ColumnDriftMetric(column_name=self.column_name),
                    TextDescriptorsDriftMetric(column_name=self.column_name, descriptors=self.descriptors),
                ]
            )
        return result
