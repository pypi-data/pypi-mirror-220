import os
import requests
import logging
from dotenv import load_dotenv


## check logging level
if os.environ.get('BLINK_LOGGING_LEVEL') is not None:
    logging.basicConfig(level=os.environ.get('BLINK_LOGGING_LEVEL'))
else:
    logging.basicConfig(level=logging.INFO)


class Blink:
    def __init__(self):
        ## if .env file exists load it
        if os.path.exists('.env'):
            load_dotenv()
        self.project_id = os.environ.get('BLINK_PROJECT_ID')
        self.token = os.environ.get('BLINK_TOKEN')
        self.base_url = os.environ.get('BLINK_BASE_URL')
        self.automation_id = os.environ.get('BLINK_AUTOMATION_ID')
        self.path_prefix = "ds"
        self.job_id = os.environ.get('BLINK_JOB_ID')
        self.timeout = 10
        self.verify_environment_variables()
        self.change_job_status('running')

    def change_job_status(self, status):
        if self.job_id is None:
            raise Exception('BLINK_JOB_ID is not set in .env file or environment variables')
        if status not in ['running','success', 'failure']:
            raise Exception('status must be success or failure')
        logging.info(f'Changing job status to {status}')
        response = requests.put(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/jobs/{self.job_id}', json={'status': status},
                                headers={'Authorization': 'Bearer ' + self.token}, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error(response)

    def update_job_logs(self, logs):
        if self.job_id is None:
            raise Exception('BLINK_JOB_ID is not set in .env file or environment variables')
        logging.info(f'Updating job logs')
        response = requests.put(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/jobs/{self.job_id}', json={'message': logs},
                                headers={'Authorization': 'Bearer ' + self.token}, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error(response)


    def verify_environment_variables(self):
        if self.project_id is None:
            raise Exception('BLINK_PROJECT_ID is not set in .env file or environment variables')
        if self.token is None:
            raise Exception('BLINK_TOKEN is not set in .env file or environment variables')
        if self.base_url is None:
            raise Exception('BLINK_BASE_URL is not set in .env file or environment variables')
        if self.automation_id is None:
            raise Exception('BLINK_AUTOMATION_PACKAGE_ID is not set in .env file or environment variables')

    def handle_error(self, response):
        if response.status_code == 401:
            raise Exception('Unauthorized, check your token')
        elif response.status_code == 404:
            raise Exception('Not found, check your project id')
        elif response.status_code == 500:
            raise Exception('Internal server error', response.text)
        else:
            raise Exception('Unknown error')
        

    def list_secrets(self):
        logging.info('Listing secrets')
        response = requests.get(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/secrets',
                                headers={'Authorization': 'Bearer ' + self.token}, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error(response)

    def list_documents(self):
        response = requests.get(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/documents',
                                headers={'Authorization': 'Bearer ' + self.token}, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error(response)

    def get_secret(self, secret_id):
        logging.info(f'Getting secret {secret_id}')
        response = requests.get(
            f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/secrets/{secret_id}',
            headers={'Authorization': 'Bearer ' + self.token}, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error(response)

    def create_secret(self, secret_name, secret_description, secret_data):
        ## validate secret data is a dictionary
        if type(secret_data) is not dict:
            raise Exception('secret_data must be a dictionary')
        if secret_name is None:
            raise Exception('secret_name is required')
        body = {"name": secret_name, "description": secret_description, "data": secret_data}
        response = requests.post(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/secrets', json=body,
                                headers={'Authorization': 'Bearer ' + self.token}, timeout=self.timeout)
        if response.status_code == 201:
            logging.info(f'Created secret {secret_name}')
            return response.json()
        else:
            self.handle_error(response)

    def get_document(self, document_id):
        response = requests.get(
            f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/documents/{document_id}',
            headers={'Authorization': 'Bearer ' + self.token}, timeout=self.timeout)
        if response.status_code == 200:
            ## return the content of the document binary
            return response.content, response.headers['Content-Type']
        else:
            self.handle_error(response)

    def set_secrets_to_environment_variables(self):
        secrets = self.list_secrets()
        for secret in secrets:
            for key, value in self.get_secret(secret['id'])['data'].items():
                ## format as all caps and remove spaces
                key = key.upper().replace(' ', '_')
                logging.info(f'Setting {key} to environment variable')
                os.environ[key] = value

            