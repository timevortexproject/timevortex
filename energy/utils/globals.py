#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Globals"""

KEY_CURRENTCOST = "currentcost"
KEY_ENERGY = "energy"
ERROR_CC_BAD_PORT = "currentcost_bad_port"
ERROR_CC_NO_MESSAGE = "currentcost_no_message"
ERROR_CC_DISCONNECTED = "currentcost_disconnected"
ERROR_CC_INCORRECT_MESSAGE = "currentcost_incorrect_message"
ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR = "currentcost_incorrect_message_missing_tmpr"
ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS = "currentcost_incorrect_message_missing_watts"
ERROR_CURRENTCOST = {
    ERROR_CC_BAD_PORT: "CurrentCost %s in %s: TTY problem: %s is unreachable. Retry connection in %s seconds.",
    ERROR_CC_NO_MESSAGE: "CurrentCost %s in %s: Reach timeout. Verify CurrentCost wire connection or wave range",
    ERROR_CC_DISCONNECTED: "CurrentCost %s in %s: TTY port %s disconnected.",
    ERROR_CC_INCORRECT_MESSAGE: "CurrentCost %s in %s: Send incorrect message => %s.",
    ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR: "CurrentCost %s in %s: Missing currentcost temperature value in %s",
    ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS: "CurrentCost %s in %s: Missing currentcost watts value in %s",
}
TTY_CONNECTION_SUCCESS = "CurrentCost %s in %s: Success connection to %s."
CURRENTCOST_UNICODE_ERROR = "Bad message sent from currentcost, invalid ASCII"
