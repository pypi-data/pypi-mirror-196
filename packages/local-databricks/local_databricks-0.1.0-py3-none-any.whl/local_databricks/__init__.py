# -*- coding: utf-8 -*-
"""Top level package for local_databricks."""

from local_databricks.logger import configure_logging
from local_databricks.settings import init_settings


SETTINGS = init_settings()

logger = configure_logging(
   "local_databricks", SETTINGS, kidnap_loggers=True
)
