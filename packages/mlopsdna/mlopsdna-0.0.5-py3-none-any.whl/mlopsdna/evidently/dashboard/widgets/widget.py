#!/usr/bin/env python
# coding: utf-8
import abc
from typing import Optional

import pandas as pd

from mlopsdna.evidently import ColumnMapping
from mlopsdna.evidently.model.widget import BaseWidgetInfo
from mlopsdna.evidently.options import OptionsProvider


class Widget:
    title: str
    wi: Optional[BaseWidgetInfo]
    options_provider: OptionsProvider

    def __init__(self, title: str):
        self.title = title
        self.wi = None

    @abc.abstractmethod
    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        raise NotImplementedError()

    @abc.abstractmethod
    def analyzers(self):
        return []
