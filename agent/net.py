import os

import agent.configuration as config
import agent.utils.log as log
import deps.requests as requests

from agent.operation import MessageKey, OperationType


class RequestMethod:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'


# This dictionary is updated on a refresh_response_uri operation
ResponseDict = {
    OperationType.REFRESH_RESPONSE_URIS: {
        MessageKey.RESPONSE_URI: 'rvl/v2/core/uris/response',
        MessageKey.REQUEST_METHOD: RequestMethod.GET
    }
}


def get_response_uri(operation_type):
    """Get the appropriate uri to respond to for the corresponding
    operation type.

    Args:
        operation_type (str): The operation type you're looking a
            uri for.

    Returns:
        (str): The uri corresponding to the operation type
    """
    response_uri = ResponseDict \
                   .get(operation_type, {}) \
                   .get(MessageKey.RESPONSE_URI, '')

    return response_uri.format(config.AGENT_ID)


def get_request_method(operation_type):
    """Get the appropriate request method to use to respond to the server with
    depending on the operation type.

    Args:
        operation_type (str): The operation type you're looking a
            request method for.

    Returns:
        (str): The request method corresponding to the operation type
    """
    return ResponseDict \
           .get(operation_type, {}) \
           .get(MessageKey.REQUEST_METHOD, '')


def _get_callable_request_method(req_method):
    """Use to get the appropriate request method to talk to the server.

    Args:
        (str) req_method: The request method that is wanted
            (Ex: POST, PUT, GET)

    Returns:
        (func/Exception) The corresponding requests method that matches
        what was passed in arguments. Throws an exception if no request
        method found.
    """
    if req_method.upper() == RequestMethod.POST:
        return requests.post
    if req_method.upper() == RequestMethod.PUT:
        return requests.put
    if req_method.upper() == RequestMethod.GET:
        return requests.get

    raise Exception(
        "Could not get request method for {0}"
        .format(req_method)
    )


def send_message(message, uri, req_method):
    """Sends a message to the server and waits for data in return.

    Args:
        message (str): JSON formatted str to send the server.
        uri (str): RESTful uri to send the message.
        req_method (str): HTTP Request Method

    Returns:
        (bool, dict): A tuple that contains the success (bool) from sending
        the message which is True if the status code is 200, False
        otherwise, and a dictionary containing the response from the server.
    """
    server_url = 'https://{0}:{1}/'.format(
        config.SERVER_ADDRESS, config.SERVER_PORT
    )

    url = os.path.join(server_url, uri)
    headers = {
        'Content-type': 'application/json',
        'Authorization': {
            'token': config.TOKEN
        }
    }

    sent = False
    received_data = {}

    log.debug("Sending message to: {0}".format(url))

    try:
        request_method = _get_callable_request_method(req_method)

        response = request_method(
            url,
            data=message,
            headers=headers,
            verify=False,
            timeout=30
        )

        log.debug("Status code: {0}".format(response.status_code))
        log.debug("Server text: {0}".format(response.text))

        if response.status_code == 200:
            sent = True

        try:
            received_data = response.json()

        except Exception as exc:
            log.error("Unable to read data from server. Invalid JSON?")
            log.exception(exc)

    except Exception as exc:
        log.error("Unable to send data to server.")
        log.exception(exc)

    return sent, received_data


def send_operation_message(message, operation_type):
    """A wrapper function on the send_message function that gets the
    response uri and request method based solely on the operation type
    passed in argument.

    Args:
        message (str): The message to be sent, if any.
        operation_type (str): The type of operation for which this message
            belongs.

    Returns:
        Please check the send_message function.

    Exception:
        If the method cannot find the response uri or request method
        for the operation then an IOError exception is raised.
    """
    response_uri = get_response_uri(operation_type)
    request_method = get_request_method(operation_type)

    if not (response_uri and request_method):
        raise IOError(
            "Could not find response uri and/or request method for {0}. "
            "response_uri: {1}, request_method: {2}".format(
                operation_type, response_uri, request_method
            )
        )

    return send_message(message, response_uri, request_method)
