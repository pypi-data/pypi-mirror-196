#!/usr/bin/env python
# coding: utf-8
from mlopsdna.evidently.dashboard.tabs.base_tab import Tab
from mlopsdna.evidently.dashboard.tabs.base_tab import Verbose
from mlopsdna.evidently.dashboard.widgets.data_drift_table_widget import DataDriftTableWidget


class DataDriftTab(Tab):
    widgets = [(DataDriftTableWidget("Data Drift"), Verbose.ALWAYS)]
