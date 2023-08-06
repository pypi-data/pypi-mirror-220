# Create your views here.
import logging
import json
import jsonschema
from pathlib import Path

logger = logging.getLogger("info_logs")
logger_error = logging.getLogger('error_logs')


def schema_validation(data, path):
    """Function for validating Json Schema functionality."""
    try:
        flag = 0
        schema = load(path)
        logger.info(schema)
        data = data.get_json()
        v = jsonschema.Draft4Validator(schema)
        logger.info(v)
        errors = sorted(v.iter_errors(data), key=lambda e: e.path)
        for error in errors:
            logger.info('json validation failed')
            flag = 452
            output_json = dict(zip(['Status', 'Message', 'Payload'], [flag, error.message, None]))
            return output_json
        logger.info('schema validation done')
        output_json = dict(zip(['Status', 'Message', 'Payload'], [flag, 'schema validation done', None]))
        return output_json
    except Exception as ex:
        logger_error.error(f"Exception Encountered Exception is : {ex}", exc_info=1)
        output_json = dict(zip(['Status', 'Message', 'Payload'], [500, f"Exception encountered: {ex}", None]))
        return output_json


def load(schema_path):
    """
    :param schema_path:
    :return:
    """
    schema = Path(schema_path)

    with schema.open() as f:
        return json.load(f)
