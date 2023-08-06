# -*- coding: utf-8 -*-
"""Database connection and session handle."""

from local_databricks import SETTINGS, logger
from local_databricks.settings import __app_name__
from pyspark.sql import SparkSession

# pylint: disable=no-member


# Create SparkSession from builder
def create_local_spark_session():
    logger.info("Creating local spark session")
    SPARK = SparkSession \
        .builder \
        .appName(__app_name__) \
        .master('local[*]') \
        .getOrCreate()
    return SPARK

def get_spark_session(): # run only once
    if SETTINGS.DATABRICKS:
        logger.info("Getting databricks spark session")
        return globals()['spark']
    else:
        return create_local_spark_session()
    
def get_databricks_display():
    if SETTINGS.DATABRICKS:
        logger.info("Getting databricks display")
        return globals()['display']
    else:
        return False

def get_databricks_dbutils():
    logger.info("Getting databricks dbutils")
    if SETTINGS.DATABRICKS:
        return globals()['dbutils']
    else:
        return None


SPARK = get_spark_session() # spark session
DISPLAY = get_databricks_display() # display
DBUTILS = get_databricks_dbutils() # dbutils


if __name__ == "__main__":
    pass
