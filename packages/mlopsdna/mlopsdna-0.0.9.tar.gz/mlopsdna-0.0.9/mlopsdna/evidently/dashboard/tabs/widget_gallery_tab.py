from mlopsdna.evidently.dashboard.tabs.base_tab import Tab
from mlopsdna.evidently.dashboard.tabs.base_tab import Verbose
from mlopsdna.evidently.dashboard.widgets.bar_widget import BarWidget
from mlopsdna.evidently.dashboard.widgets.counter_widget import CounterWidget
from mlopsdna.evidently.dashboard.widgets.expandable_list_widget import ExpandableListWidget
from mlopsdna.evidently.dashboard.widgets.percent_widget import PercentWidget
from mlopsdna.evidently.dashboard.widgets.test_suite_widget import TestSuiteWidget
from mlopsdna.evidently.dashboard.widgets.text_widget import TextWidget


class WidgetGalleryTab(Tab):
    widgets = [
        (BarWidget(""), Verbose.ALWAYS),
        (CounterWidget(""), Verbose.ALWAYS),
        (PercentWidget(""), Verbose.ALWAYS),
        (ExpandableListWidget("Some title"), Verbose.ALWAYS),
        (TextWidget("Some title"), Verbose.ALWAYS),
        (TestSuiteWidget(""), Verbose.ALWAYS),
    ]
