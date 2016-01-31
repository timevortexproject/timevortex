#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Globals"""

KEY_CURRENTCOST = "currentcost"
KEY_ENERGY = "energy"
ERROR_CC_BAD_PORT = "currentcost_bad_port"
ERROR_CC_NO_MESSAGE = "currentcost_no_message"
ERROR_CC_DISCONNECTED = "currentcost_disconnected"
ERROR_CURRENTCOST = {
    ERROR_CC_BAD_PORT: "CurrentCost %s in %s: TTY problem: %s is unreachable. Retry connection in %s seconds.",
    ERROR_CC_NO_MESSAGE: "CurrentCost %s in %s: Reach timeout. Verify CurrentCost wire connection or wave range",
    ERROR_CC_DISCONNECTED: "CurrentCost %s in %s: TTY port %s disconnected.",
}
TTY_CONNECTION_SUCCESS = "CurrentCost %s in %s: Success connection to %s."