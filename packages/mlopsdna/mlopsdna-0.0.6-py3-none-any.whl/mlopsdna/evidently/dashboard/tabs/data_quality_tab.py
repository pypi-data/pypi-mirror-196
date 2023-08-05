#!/usr/bin/env python
# coding: utf-8
from mlopsdna.evidently.dashboard.tabs.base_tab import Tab
from mlopsdna.evidently.dashboard.tabs.base_tab import Verbose
from mlopsdna.evidently.dashboard.widgets.data_quality_correlations import DataQualityCorrelationsWidget
from mlopsdna.evidently.dashboard.widgets.data_quality_features_widget import DataQualityFeaturesWidget
from mlopsdna.evidently.dashboard.widgets.data_quality_summary_widget import DataQualitySummaryWidget


class DataQualityTab(Tab):
    widgets = [
        (DataQualitySummaryWidget("Data Summary"), Verbose.ALWAYS),
        (DataQualityFeaturesWidget("Features"), Verbose.ALWAYS),
        (DataQualityCorrelationsWidget("Correlations"), Verbose.FULL),
    ]
