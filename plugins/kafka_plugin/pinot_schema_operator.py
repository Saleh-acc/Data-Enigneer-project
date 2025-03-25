import glob
from typing import Any

import requests
from airflow.models import BaseOperator
from airflow.utils.context import Context
from airflow.utils.decorators import apply_defaults
import six
import sys

class PinotSchemaSubmitOperator(BaseOperator):

    @apply_defaults
    def __init__(self, folder_path, pinot_url, *args, **kwargs):
        super(PinotSchemaSubmitOperator,self).__init__(*args, **kwargs)

        self.folder_path = folder_path
        self.pinot_url = pinot_url


    def execute(self, context: Context) -> Any:

        try:
            schema_files = glob.glob(self.folder_path + '/*.json')  # return any path that is json object in the path folder
            for schema_file in schema_files:

                with open(schema_file, 'r') as f:
                    schema_data = f.read()
                    #define the header and submit the post request to pinot

                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(self.pinot_url, headers=headers, data=schema_data)

                    if response.status_code == 200:
                        self.log.info(f'Schema successfully submitted toApache Pinot! {schema_file}')
                    else:
                        self.log.error(f'Failed to submit schema: {response.status_code} - {response.text}')
                        raise Exception(f'Schema submission failed with satus code {response.status_code}')

        except Exception as e:
            self.log.error(f'An error occurred: {str(e)}')

