#!/usr/bin/env python
# coding: utf-8

from dataclasses import dataclass
from typing import List

from mlopsdna.evidently.model.widget import BaseWidgetInfo


@dataclass
class DashboardInfo:
    name: str
    widgets: List[BaseWidgetInfo]
