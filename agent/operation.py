import json
import time

import agent.utils.misc_utils as misc
import agent.utils.variables as gvars


class MessageKey:
    """Keys for encoding/decoding messages in JSON from/to server."""
    OPERATION = 'operation'
    OPERATION_ID = 'operation_id'
    PLUGIN = 'plugin'
    DATA = 'data'

    # Not naming as 'OPERATIONS' due to easily confusing with 'OPERATION'
    OPERATION_LIST = 'operations'

    AGENT_ID = 'agent_id'
    RESPONSE_URI = 'response_uri'
    REQUEST_METHOD = 'request_method'

    REBOOTED = 'rebooted'
    SYSTEM_INFO = 'system_info'
    HARDWARE_INFO = 'hardware'
    PLUGINS = 'plugins'

    AGENT_ID = 'agent_id'
    VIEWS = 'views'
    TAGS = 'tags'

    OPERATION_SUCCESS = 'success'
    OPERATION_RESULT_MESSAGE = 'message'

    SHUTDOWN_DELAY_SECONDS = 'shutdown_delay_seconds'
    REBOOT_DELAY_SECONDS = 'reboot_delay_seconds'


class OperationType:
    """The operation types known by the agent."""
    NEW_AGENT = 'new_agent'
    NEW_AGENT_ID = 'new_agent_id'
    STARTUP = 'startup'
    REBOOT = 'reboot'
    SHUTDOWN = 'shutdown'
    INVALID_AGENT_ID = 'invalid_agent_id'
    CHECK_IN = 'check_in'
    REFRESH_RESPONSE_URIS = 'refresh_response_uris'

    RESULT = 'result'


class Operation(object):
    """Represents an operation to be run by the agent."""

    def __init__(self, message=None, op_dict=None):
        """Create an operation object which represents an operation to be run
        by the agent. An operation can also be loaded from a JSON message or a
        dictionary which defines all the user-defined attributes.

        Args:
            message (str): JSON message containing operation details.
            op_dict (dict): Dictionary containing keys that represent all
                the attributes for this object. Similar/exactly to what you
                retrieve from self.to_dict().
        """
        self.type = None
        self.id = None
        self.plugin = None # The plugin this operation corresponds to
        self.data = None # Contains all data relevant to the operation

        # Result is filled in with the results after the operation finishes
        self.result = None

        if message:
            self._load_message(message)
        elif op_dict:
            self.__dict__ = dict(self.__dict__.items() + op_dict.items())
        else:
            self.id = self._self_assigned_id()

    def _self_assigned_id(self):
        """Appends special string after uuid to denote self generated id.

        Returns:
            (str): uuid generated from misc utils with a hardcoded string
            appended to the end to denote that it has been self generated.
        """
        return misc.generate_uuid() + gvars.SELF_GENERATED_OP_ID

    def _load_message(self, message):
        """Fill in the attributes of this object with the received message."""
        json_message = json.loads(message)

        self.type = json_message.get(MessageKey.OPERATION)
        self.id = json_message.get(
            MessageKey.OPERATION_ID, self._self_assigned_id()
        )
        self.plugin = json_message.get(MessageKey.PLUGIN)
        self.data = json_message.get(MessageKey.DATA, {})

    def is_savable(self):
        """Specifies whether this operation should be saved on agent shutdown.

        Returns:
            (bool): True or False on whether the operation is savable or not
        """

        # TODO: figure out what operations should be saved
        savable = []

        return self.type in savable

    def to_dict(self):
        """Get all user-defined attributes of this object.

        Returns:
            (dict): All user-defined attributes directly from the __dict__
                method.
        """
        return self.__dict__

    def log_print(self):
        """2-Tuple with some information specific to this Operation for logging
        purposes.

        Returns:
            (str): Returns back a tuple wrapped as a string that has elements:
                (operation type, operation id)
        """
        return "({0}, {1})".format(self.type, self.id)


class ResultOperation(object):
    """Acts as a wrapper for Operations; adding functionality needed when
       attempting to send results to server.
        
       Allows you to set a timeout for sending results back. Presumably this
       result cannot be sent to server unless the current time since epoch is
       greater than that set in wait_until.
    """

    def __init__(self, operation, retry):
        """
        Args:
            operation (Operation): The operation containing the result to
                be sent to the server.

            retry (bool): Tells the result loop whether or not to retry sending
                results if a failure occurs on an attempt.
        """

        self.id = self._self_assigned_id()
        self.type = operation.type
        self.result = operation.result
        self.retry = retry

        # Sets current time. Meaning there is no wait to send result
        self.wait_until = self._time_in_seconds()

    def _time_in_seconds(self):
        """
        Returns:
            (int) current time in seconds since epoch.
        """
        return int(time.time())

    def timeout(self, seconds=60):
        """Timeout this result by the amount specified in seconds."""
        self.wait_until = self._time_in_seconds() + seconds

    def should_be_sent(self):
        """Says whether this result should be sent to server.
        
        Returns:
            (bool): True if should be sent, False otherwise.
        """

        if self._time_in_seconds() > self.wait_until:
            return True

        return False

    def is_savable(self):
        """Specifies whether this operation should be saved to file for
        recovery.

        Returns:
            (bool): True or False on whether the operation is savable or not
        """
        # TODO: figure out what operations should be saved
        savable = []

        return self.type in savable

    def _self_assigned_id(self):
        """Appends special string after uuid to denote self generated id.
        
        Returns:
            (str): uuid generated from misc utils with a hardcoded string
            appended to the end to denote that it has been self generated.
        """
        return misc.generate_uuid() + gvars.SELF_GENERATED_OP_ID

    def to_dict(self):
        return {
            'operation_type': self.type,
            'operation_result': self.result,
            'wait_until': self.wait_until
        }

    def log_print(self):
        """2-Tuple with some information specific to this Operation for logging
        purposes.

        Returns:
            (str): Returns back a tuple wrapped as a string that has elements:
                (operation type, operation id)
        """
        return "({0}, {1})".format(self.type, self.id)
