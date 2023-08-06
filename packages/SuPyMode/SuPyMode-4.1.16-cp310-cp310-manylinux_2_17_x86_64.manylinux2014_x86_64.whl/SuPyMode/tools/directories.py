#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path

import SuPyMode

RootPath = Path(SuPyMode.__path__[0])

ReportPath = os.path.join(RootPath.parents[0], 'Reports')

example_directory = os.path.join(RootPath, 'examples')

instance_directory = os.path.join(RootPath, 'superset_instances/')

reports_directory = os.path.join(RootPath, 'reports/')

validation_data_path = os.path.join(RootPath, 'validation_data')

temporary_image_path = os.path.join(RootPath.parents[0], 'temporary_data')

# -
