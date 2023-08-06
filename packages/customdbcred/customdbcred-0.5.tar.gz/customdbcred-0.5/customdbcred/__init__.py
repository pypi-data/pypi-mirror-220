# Custom Module to fetch database credentials
import logging
import json
from functools import wraps

from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

logger_error = logging.getLogger('error_logs')


def get_db_cred(func):
    @wraps(func)
    def wrapper_func(req):
        try:
            if type(req) == dict:
                result = func(req)
                return result
            keyVaultName = "myappkv"
            KVUri = f"https://{keyVaultName}.vault.azure.net"
            # credential = DefaultAzureCredential()
            credential = ClientSecretCredential(tenant_id='26afc1b1-8393-439d-aa1a-483105d77dc3',
                                                client_id='9d2fe19f-47e6-498f-b384-6f94b0d55500',
                                                client_secret='yXK8Q~3IJa1qOKpF5NyoQNdCsz63ugQEUIutpdv-')
            client = SecretClient(vault_url=KVUri, credential=credential)
            dbcred = client.get_secret("DATABASECRED").value
            cred = json.loads(dbcred)
            # server = client.get_secret("SERVER").value
            # database = client.get_secret("DATABASE").value
            # username = client.get_secret("USERNAME").value
            # password = client.get_secret("PASSWORD").value
            server,database,username,password = cred['SERVER'], cred['DATABASE'], cred['USERNAME'], cred['PASSWORD']
            driver = '{ODBC Driver 17 for SQL Server}'
            output_json = dict(zip(["server", "database", "username", "password", "driver"],
                                   [server, database, username, password, driver]))
            request_data = req.get_json()
            request_data.update(output_json)
            result = func(request_data)
            return result
        except Exception as ex:
            logger_error.error(f"Exception Encountered Exception is : {ex}", exc_info=1)
            output_json = dict(zip(['Status', 'Message', 'Payload'], [500, f"Exception encountered: {ex}", None]))
            result = func(output_json)
            return func(result)
    return wrapper_func