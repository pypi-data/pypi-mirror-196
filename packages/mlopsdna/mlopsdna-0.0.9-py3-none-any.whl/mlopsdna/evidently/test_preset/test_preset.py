import abc

from mlopsdna.evidently.base_metric import InputData
from mlopsdna.evidently.utils.data_operations import DatasetColumns


class TestPreset:
    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        raise NotImplementedError()
