from enum import Enum


class Successful(Enum):
    """Http Successful Status Codes"""
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_202_ACCEPTED = 202
    HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203
    HTTP_204_NO_CONTENT = 204
    HTTP_205_RESET_CONTENT = 205
    HTTP_206_PARTIAL_CONTENT = 206
    HTTP_207_MULTI_STATUS = 207
    HTTP_208_ALREADY_REPORTED = 208
    HTTP_226_IM_USED = 226

    @staticmethod
    def list():
        # return list(map(lambda c: c.value, Color))
        lst = list(map(lambda status: status.value, Successful))
        keylist = ['HTTP_200_OK', 'HTTP_201_CREATED', 'HTTP_202_ACCEPTED', 'HTTP_203_NON_AUTHORITATIVE_INFORMATION',
                   'HTTP_204_NO_CONTENT', 'HTTP_205_RESET_CONTENT', 'HTTP_206_PARTIAL_CONTENT', 'HTTP_207_MULTI_STATUS',
                   'HTTP_208_ALREADY_REPORTED', 'HTTP_226_IM_USED']

        d = dict(zip(keylist, lst))
        return d


class Informational(Enum):
    """ Http Authentication Status Codes"""
    HTTP_100_CONTINUE = 100
    HTTP_101_SWITCHING_PROTOCOLS = 101

    @staticmethod
    def list():
        # return list(map(lambda c: c.value, Color))
        lst = list(map(lambda status: status.value, Informational))
        keylist = ['HTTP_100_CONTINUE', 'HTTP_101_SWITCHING_PROTOCOLS']
        d = dict(zip(keylist, lst))
        return d


class Redirection(Enum):
    """ Http Redirection Status Codes"""
    HTTP_300_MULTIPLE_CHOICES = 300
    HTTP_301_MOVED_PERMANENTLY = 301
    HTTP_302_FOUND = 302
    HTTP_303_SEE_OTHER = 303
    HTTP_304_NOT_MODIFIED = 304
    HTTP_305_USE_PROXY = 305
    HTTP_306_RESERVED = 306
    HTTP_307_TEMPORARY_REDIRECT = 307
    HTTP_308_PERMANENT_REDIRECT = 308

    @staticmethod
    def list():
        # return list(map(lambda c: c.value, Color))
        lst = list(map(lambda status: status.value, Redirection))
        keylist = ['HTTP_300_MULTIPLE_CHOICES', 'HTTP_301_MOVED_PERMANENTLY', 'HTTP_302_FOUND', 'HTTP_303_SEE_OTHER',
                   'HTTP_304_NOT_MODIFIED',
                   'HTTP_305_USE_PROXY', 'HTTP_306_RESERVED', 'HTTP_307_TEMPORARY_REDIRECT',
                   'HTTP_308_PERMANENT_REDIRECT']
        d = dict(zip(keylist, lst))
        return d


class SarciInternalStatusCodes(Enum):
    """ Karza Internal Http Calls"""
    HTTP_200_OK = {'status': 200, 'message': 'OK'}
    HTTP_400_BAD_REQUEST = {'status': 400, 'message': 'Bad Request'}
    HTTP_401_UNAUTHORIZED_ACEESS = {'status': 401, 'message': 'Unauthorized Access'}
    HTTP_402_INSUFFICIENT_CREDITS = {'status': 402, 'message': 'Insufficient Credits'}
    HTTP_500_INTERNAL_SERVER_ERROR = {'status': 500, 'message': 'Internal Server Error'}
    HTTP_503_SOURCE_UNAVAIlABLE = {'status': 503, 'message': 'Source Unavailable'}
    HTTP_504_ENDPOINT_REQUEST_TIMED_OUT = {'status': 504, 'message': 'Endpoint Request Timed Oute'}
    HTTP_101_VALID_AUTHENTICATION = {'status': 101, 'message': 'Valid Authentication'}
    HTTP_102_INVALID_ID_NUMBER_OR_COMBINATION_OF_INPUTS = {'status': 102,
                                                           'message': 'Invalid ID number or combination of inputs'}
    HTTP_103_NO_RECORDS_FOUND = {'status': 103, 'message': 'No records found for the given ID or combination of inputs'}
    HTTP_104_MAX_RETRIES_EXCEEDED = {'status': 104, 'message': 'Max retries exceeded'}
    HTTP_105_MISSING_CONSENT = {'status': 105, 'message': 'Missing Consent'}
    HTTP_106_MULTIPLE_RECORDS_EXIST = {'status': 106, 'message': 'Multiple Records Exist'}
    HTTP_107_NOT_SUPPORTED = {'status': 107, 'message': 'Not Supported'}
    HTTP_108_INTERNAL_SOURCE_UNAVAILABLE = {'status': 108, 'message': 'Not Supported'}
    HTTP_109_TOO_MANY_RECORDS_FOUND = {'status': 109, 'message': 'Not Supported'}

    @staticmethod
    def list():
        lst = list(map(lambda status_name: status_name.value, SarciInternalStatusCodes))
        return lst


class ClientError(Enum):
    """ Http Request Error Status Codes"""
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_402_PAYMENT_REQUIRED = 402
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_405_METHOD_NOT_ALLOWED = 405
    HTTP_406_NOT_ACCEPTABLE = 406
    HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407
    HTTP_408_REQUEST_TIMEOUT = 408
    HTTP_409_CONFLICT = 409
    HTTP_410_GONE = 410
    HTTP_411_LENGTH_REQUIRED = 411
    HTTP_412_PRECONDITION_FAILED = 412
    HTTP_413_REQUEST_ENTITY_TOO_LARGE = 413
    HTTP_414_REQUEST_URI_TOO_LONG = 414
    HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
    HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE = 416
    HTTP_417_EXPECTATION_FAILED = 417
    HTTP_422_UNPROCESSABLE_ENTITY = 422
    HTTP_423_LOCKED = 423
    HTTP_424_FAILED_DEPENDENCY = 424
    HTTP_426_UPGRADE_REQUIRED = 425
    HTTP_428_PRECONDITION_REQUIRED = 428
    HTTP_429_TOO_MANY_REQUESTS = 429
    HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = 451

    @staticmethod
    def list():
        # return list(map(lambda c: c.value, Color))
        lst = list(map(lambda status: status.value, ClientError))
        keylist = ['HTTP_400_BAD_REQUEST', 'HTTP_401_UNAUTHORIZED', 'HTTP_402_PAYMENT_REQUIRED', 'HTTP_403_FORBIDDEN',
                   'HTTP_404_NOT_FOUND', 'HTTP_405_METHOD_NOT_ALLOWED', 'HTTP_406_NOT_ACCEPTABLE',
                   'HTTP_407_PROXY_AUTHENTICATION_REQUIRED', 'HTTP_408_REQUEST_TIMEOUT', 'HTTP_409_CONFLICT',
                   'HTTP_410_GONE', 'HTTP_411_LENGTH_REQUIRED', 'HTTP_412_PRECONDITION_FAILED',
                   'HTTP_413_REQUEST_ENTITY_TOO_LARGE', 'HTTP_414_REQUEST_URI_TOO_LONG',
                   'HTTP_415_UNSUPPORTED_MEDIA_TYPE', 'HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE',
                   'HTTP_417_EXPECTATION_FAILED', 'HTTP_422_UNPROCESSABLE_ENTITY', 'HTTP_423_LOCKED',
                   'HTTP_424_FAILED_DEPENDENCY', 'HTTP_426_UPGRADE_REQUIRED',
                   'HTTP_428_PRECONDITION_REQUIRED', 'HTTP_429_TOO_MANY_REQUESTS',
                   'HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE', 'HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS'
                   ]
        d = dict(zip(keylist, lst))
        return d


class ServerError(Enum):
    """Http Internal Server Error Status Codes"""
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_501_NOT_IMPLEMENTED = 501
    HTTP_502_BAD_GATEWAY = 502
    HTTP_503_SERVICE_UNAVAILABLE = 503
    HTTP_504_GATEWAY_TIMEOUT = 504
    HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505
    HTTP_506_VARIANT_ALSO_NEGOTIATES = 506
    HTTP_507_INSUFFICIENT_STORAGE = 507
    HTTP_508_LOOP_DETECTED = 508
    HTTP_509_BANDWIDTH_LIMIT_EXCEEDED = 509
    HTTP_510_NOT_EXTENDED = 510
    HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511

    @staticmethod
    def list():
        # return list(map(lambda c: c.value, Color))
        lst = list(map(lambda status: status.value, ServerError))
        keylist = ['HTTP_500_INTERNAL_SERVER_ERROR', 'HTTP_501_NOT_IMPLEMENTED', 'HTTP_502_BAD_GATEWAY',
                   'HTTP_503_SERVICE_UNAVAILABLE', 'HTTP_504_GATEWAY_TIMEOUT',
                   'HTTP_505_HTTP_VERSION_NOT_SUPPORTED', 'HTTP_506_VARIANT_ALSO_NEGOTIATES',
                   'HTTP_507_INSUFFICIENT_STORAGE', 'HTTP_508_LOOP_DETECTED', 'HTTP_509_BANDWIDTH_LIMIT_EXCEEDED',
                   'HTTP_510_NOT_EXTENDED', 'HTTP_511_NETWORK_AUTHENTICATION_REQUIRED']
        d = dict(zip(keylist, lst))
        return d


def aggregate_status_codes():
    """ Get aggregate of all status codes with keys and values """
    d1, d2, d3, d4, d5 = Successful.list(), Informational.list(), Redirection.list(), ClientError.list(), ServerError.list()
    d1.update(d2)
    d1.update(d3)
    d1.update(d4)
    d1.update(d5)
    return d1


def get_status_code_name(pattern):
    """ Get the key for status codes"""
    status_codes_dic = aggregate_status_codes()
    for k, v in status_codes_dic.items():
        if v == pattern:
            return k
