from mlopsdna.evidently.base_metric import InputData
from mlopsdna.evidently.test_preset.test_preset import TestPreset
from mlopsdna.evidently.tests import TestValueMAE
from mlopsdna.evidently.tests import TestValueMAPE
from mlopsdna.evidently.tests import TestValueMeanError
from mlopsdna.evidently.tests import TestValueRMSE
from mlopsdna.evidently.utils.data_operations import DatasetColumns


class RegressionTestPreset(TestPreset):
    """
    Regression performance tests.

    Contains tests:
    - `TestValueMeanError`
    - `TestValueMAE`
    - `TestValueRMSE`
    - `TestValueMAPE`
    """

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestValueMeanError(),
            TestValueMAE(),
            TestValueRMSE(),
            TestValueMAPE(),
        ]
