
import json
import os
import sys
import argparse

from local_databricks import SETTINGS, logger
# from local_databricks.session import DBUTILS, DISPLAY, SPARK


def display(obj):
	if SETTINGS.DATABRICKS:
		DISPLAY(obj)
	else:
		# display local
		print(obj)


def get_secret(key: str, scope: str):
	logger.info(f"Getting secret {key} from scope {scope}")
	if SETTINGS.DATABRICKS:
		return DBUTILS.secrets.get(scope=scope, key=key)
	else:
		# get local secret
		return os.environ[key]  # TODO: find a better way to do this


def set_enviroment(key: str, value: str):
	logger.info(f"Setting enviroment {key} to {value}")
	if SETTINGS.DATABRICKS:
		SPARK.conf.set(key, value)
	else:
		# set local enviroment
		os.environ[key] = value


def read_enviroment(key: str):
	logger.info(f"Reading enviroment {key}")
	if SETTINGS.DATABRICKS:
		return SPARK.conf.get(key)
	else:
		# get local enviroment
		return os.environ[key]

def run_notebook(path: str, timeout_seconds: int, arguments: dict):
	logger.info(f'Running python {path} with arguments "{arguments}"')
	if SETTINGS.DATABRICKS:
		DBUTILS.notebook.run(path, timeout_seconds, arguments=arguments)
	else:
		# run local notebook
		# kwargs = json.dumps(arguments)
		kwargs = ""
		for k,v in arguments.items():
			kwargs += f"{k}:{v},"
		kwargs = kwargs[:-1]

		os.system(f"""python {path} --fieldMap "{kwargs}" """)
		
def get_notebook_params():
	logger.info(f"Getting notebook input params")
	if SETTINGS.DATABRICKS:
		return dict(DBUTILS.notebook.entry_point.getCurrentBindings())
	else:
		# get local notebook params
		parser = argparse.ArgumentParser()
		parser.add_argument('--fieldMap',
					type=lambda x: {k:v for k,v in (i.split(':') for i in x.split(','))},
					help='comma-separated key:value pairs, e.g. Date:0,Amount:2,Payee:5,Memo:9'
				)
		return parser.parse_args().fieldMap


if __name__ == "__main__":
	pass