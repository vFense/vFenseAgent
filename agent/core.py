import json
import threading

import agent.configuration as config
import agent.utils.log as log
import agent.net as net

from agent.operation import MessageKey, OperationType, Operation


class AgentCore(object):
    def __init__(self):
        self._net_handler = None

        self._allow_checkin = True
        self._checkin_timer = None

    def _agent_checkin(self):
        """Checks in to the server to retrieve all pending operations."""

        if self._allow_checkin:
            message_dict = {
                MessageKey.OPERATION: OperationType.CHECK_IN,
                MessageKey.OPERATION_ID: '', # TODO: should null be sent?
                MessageKey.AGENT_ID: config.AGENT_ID
            }

            sent, server_response = net.send_operation_message(
                json.dumps(message_dict), OperationType.CHECK_IN
            )

            if not sent:
                log.error(
                    "Could not check-in to server. Check agent and server "
                    "logs for details."
                )

            if server_response:
                self.process_server_message(server_response)

        else:
            log.debug("Checkin set to false.")


    def initialize(self):
        config.initialize()
        log.initialize()

        # TODO: Create a helper class to simplify starting/stopping this timer?
        self._checkin_timer = threading.Timer(60, self._agent_checkin)

    def start(self):
        self._checkin_timer.start()

    #def process_server_operation(self, op_dict):
    #    """Process incoming operation from server.

    #    Args:
    #        op_dict (dict): A dictionary representing an operation from
    #            the server.
    #    """
    #    try:
    #        operation = Operation(op_dict)

    #        put_front = False
    #        if operation.type == OperationType.NEW_AGENT_ID:
    #            put_front = True

    #        self.add_to_operation_queue(operation, put_front)

    #    except ValueError as err:
    #        log.error("Failed to create operation from operation dictionary.")
    #        log.exception(err)

    def process_server_message(self, message):
        """Turn the message from the server into an Operation and place in the
        operation queue to process.

        Args:
            message (str): A JSON encoded string.
        """
        print "Message: {0}".format(message)
        #try:
        #    message_dict = json.loads(message)
        #except ValueError as err:
        #    log.error("Could not decode JSON message: {0}".format(message))
        #    log.exception(err)
        #    return

        #log.debug(
        #    "Server message: {0}".format(json.dumps(message_dict, indent=4))
        #)

        #if not message_dict:
        #    return

        #for op_dict in message_dict.get(MessageKey.DATA, []):
        #    op_plugin = message_dict.get(MessageKey.PLUGIN)

        #    if not op_plugin:
        #        self.process_server_operation(op_dict)

        #    elif op_plugin in self._plugins:
        #        self._plugins[op_plugin].process_server_operation(op_dict)

        #    else:
        #        log.error(
        #            "Received unknown plugin name in message: {0}".format(
        #                op_plugin
        #            )
        #        )
