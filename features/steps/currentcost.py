#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for CurrentCost"""

import os
import shlex
import signal
import subprocess
from time import sleep
from threading import Thread
import serial
from timevortex.models import get_site_by_slug, get_variable_by_slug
from timevortex.utils.filestorage import FILE_STORAGE_SPACE
from timevortex.utils.globals import KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE
from features.steps.test_globals import SOCAT, assert_equal, assert_gte, assert_lte
from energy.management.commands.retrieve_currentcost_data import Command as CurrentCostCommand, BAUDS
from energy.utils.globals import ERROR_CC_BAD_PORT, ERROR_CC_DISCONNECTED, ERROR_CC_NO_MESSAGE
from energy.utils.globals import ERROR_CC_INCORRECT_MESSAGE, ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR
from energy.utils.globals import ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS

TIMEVORTEX_CURRENTCOST_LOG_FILE = "/tmp/timevortex/timevortex_energy.log"
TEST_CC_SITE_ID = "test_site"
TEST_CC_LABEL = "My home"
TEST_CC_VARIABLE_ID = "test_variable"
TEST_CC_VARIABLE_ID_WATTS_CH1 = "TEST_watts_ch1"
TEST_CC_VARIABLE_ID_KWH_CH1 = "TEST_kwh_ch1"
TEST_CC_VARIABLE_ID_WATTS_CH2 = "TEST_watts_ch2"
TEST_CC_VARIABLE_ID_KWH_CH2 = "TEST_kwh_ch2"
TEST_CC_VARIABLE_ID_WATTS_CH3 = "TEST_watts_ch3"
TEST_CC_VARIABLE_ID_KWH_CH3 = "TEST_kwh_ch3"
TEST_CC_VARIABLE_ID_TMPR = "TEST_tmpr"
TEST_CC_CORRECT_TTY_PORT = "/tmp/tty_currentcost"
TEST_CC_CORRECT_TTY_PORT_WRITER = "/tmp/tty_currentcost_writer"
TEST_CC_BAD_TTY_PORT = "/tmp/tty_bad"
ERROR_UNDEFINED_ERROR_TYPE = "Undefined error_type %s"
CURRENTCOST_MESSAGE = "<msg><src>CC128-v1.29</src><dsb>00786</dsb>\
<time>00:31:36</time><tmpr>19.3</tmpr><sensor>0</sensor><id>00077</id>\
<type>1</type><ch1><watts>00405</watts></ch1></msg>"
CURRENTCOST_MESSAGE_2 = "<msg><src>CC128-v1.29</src><dsb>00786</dsb>\
<time>00:31:36</time><tmpr>20.3</tmpr><sensor>0</sensor><id>00077</id>\
<type>1</type><ch1><watts>00406</watts></ch1><ch2><watts>14405</watts>\
</ch2><ch3><watts>10405</watts></ch3></msg>"
CURRENTCOST_MESSAGE_3 = "<msg><src>CC128-v1.29</src><dsb>00786</dsb>\
<time>00:31:36</time><tmpr>21.3</tmpr><sensor>0</sensor><id>00077</id>\
<type>1</type><ch1><watts>00000</watts></ch1></msg>"
WRONG_CURRENTCOST_MESSAGE = "<msg><src>ensor>0</sensor><id>00077</id>\
<type>1</type><ch1><watts>00405</watts></ch1></msg>"
INCORRECT_TMPR_CURRENTCOST_MESSAGE = "<msg><src>CC128-v1.29</src><dsb>00786</dsb>\
<time>00:31:36</time><sensor>0</sensor><id>00077</id>\
<type>1</type><ch1></ch1></msg>"
INCORRECT_WATTS_CURRENTCOST_MESSAGE = "<msg><src>CC128-v1.29</src><dsb>\
00786</dsb><tmpr>19.3</tmpr><time>00:31:36</time><sensor>0</sensor>\
<id>00077</id><type>1</type></msg>"
CC_HISTORY = "currentcost_historical_consumption"
CC_INSTANT_CONSO_1_TS_0 = "instant_consumption_1_timeseries_0"
CC_INSTANT_CONSO_2_TS_7 = "instant_consumption_2_timeseries_7"
CC_INSTANT_CONSO_1_TS_3 = "instant_consumption_1_timeseries_3"
CC_INSTANT_CONSO_2_TS_3 = "instant_consumption_2_timeseries_3"
CC_INSTANT_CONSO_2_TS_0 = "instant_consumption_2_timeseries_0"
CC_INSTANT_CONSO_3_TS_3 = "instant_consumption_3_timeseries_3"
KEY_START_VALUE = "start_value"
KEY_END_VALUE = "end_value"
KEY_END_VALUE_2 = "end_value_2"

DICT_CC_DATA_TYPE = [
    CC_INSTANT_CONSO_1_TS_0,
    CC_INSTANT_CONSO_2_TS_7,
    CC_INSTANT_CONSO_1_TS_3,
    CC_INSTANT_CONSO_2_TS_3,
    CC_INSTANT_CONSO_2_TS_0,
    CC_INSTANT_CONSO_3_TS_3,
]


def create_json_cc_value(start_value, second_value, third_value):
    """Create a json for testing purpose
    """
    return {
        CC_INSTANT_CONSO_1_TS_0: {KEY_START_VALUE: None, KEY_END_VALUE: None},
        CC_INSTANT_CONSO_2_TS_7: {KEY_START_VALUE: start_value, KEY_END_VALUE: start_value},
        CC_INSTANT_CONSO_1_TS_3: {KEY_START_VALUE: start_value, KEY_END_VALUE: second_value},
        CC_INSTANT_CONSO_2_TS_3: {KEY_START_VALUE: start_value, KEY_END_VALUE: start_value},
        CC_INSTANT_CONSO_2_TS_0: {KEY_START_VALUE: start_value, KEY_END_VALUE: start_value},
        CC_INSTANT_CONSO_3_TS_3: {KEY_START_VALUE: start_value, KEY_END_VALUE: third_value},
    }


DICT_CC_INSTANT_CONSO = {
    TEST_CC_VARIABLE_ID_WATTS_CH1: create_json_cc_value("406.0", "405.0", "0.0"),
    TEST_CC_VARIABLE_ID_KWH_CH1: {
        CC_INSTANT_CONSO_1_TS_0: {KEY_START_VALUE: None, KEY_END_VALUE: None},
        CC_INSTANT_CONSO_2_TS_7: {KEY_START_VALUE: "0.0", KEY_END_VALUE: "0.0"},
        CC_INSTANT_CONSO_1_TS_3: {KEY_START_VALUE: "0.0", KEY_END_VALUE: "0.0006", KEY_END_VALUE_2: "0.0007"},
        CC_INSTANT_CONSO_2_TS_3: {KEY_START_VALUE: "0.0", KEY_END_VALUE: "0.0012", KEY_END_VALUE_2: "0.0014"},
        CC_INSTANT_CONSO_2_TS_0: {KEY_START_VALUE: "0.0", KEY_END_VALUE: "0.0012", KEY_END_VALUE_2: "0.0014"},
        CC_INSTANT_CONSO_3_TS_3: {KEY_START_VALUE: "0.0", KEY_END_VALUE: "0.0026", KEY_END_VALUE_2: "0.0028"},
    },
    TEST_CC_VARIABLE_ID_WATTS_CH2: create_json_cc_value("14405.0", "14405.0", "14405.0"),
    TEST_CC_VARIABLE_ID_KWH_CH2: create_json_cc_value("0.0", "0.0", "0.0"),
    TEST_CC_VARIABLE_ID_WATTS_CH3: create_json_cc_value("10405.0", "10405.0", "10405.0"),
    TEST_CC_VARIABLE_ID_KWH_CH3: create_json_cc_value("0.0", "0.0", "0.0"),
    TEST_CC_VARIABLE_ID_TMPR: create_json_cc_value("20.3", "19.3", "21.3"),
}
ARRAY_CC_VARIABLE = [
    TEST_CC_VARIABLE_ID_WATTS_CH1,
    TEST_CC_VARIABLE_ID_KWH_CH1,
    TEST_CC_VARIABLE_ID_WATTS_CH2,
    TEST_CC_VARIABLE_ID_KWH_CH2,
    TEST_CC_VARIABLE_ID_WATTS_CH3,
    TEST_CC_VARIABLE_ID_KWH_CH3,
    TEST_CC_VARIABLE_ID_TMPR,
]

HISTORY_1 = "<msg><src>CC128-v1.29</src><dsb>00786</dsb><time>00:08:23</time><hist><dsw>00788</dsw><type>1</type>"\
    "<units>kwhr</units><data><sensor>0</sensor><h746>3.735</h746><h744>3.405</h744><h742>6.198</h742><h740>4.066"\
    "</h740><h738>3.152</h738><h736>1.305</h736><h734>0.251</h734><h732>0.261</h732><h730>1.575</h730><h728>0.285"\
    "</h728><h726>0.319</h726><h724>1.395</h724><h722>3.905</h722><h720>3.416</h720><h718>6.359</h718><h716>4.108"\
    "</h716><h714>3.189</h714><h712>2.094</h712><h710>0.260</h710><h708>0.258</h708><h706>1.518</h706><h704>0.261"\
    "</h704><h702>0.262</h702><h700>3.153</h700><h698>4.242</h698><h696>3.452</h696><h694>5.979</h694><h692>4.257"\
    "</h692><h690>3.173</h690><h688>1.653</h688><h686>0.261</h686><h684>0.263</h684><h682>1.333</h682><h680>0.283"\
    "</h680><h678>0.250</h678><h676>2.511</h676><h674>2.857</h674><h672>2.733</h672><h670>5.260</h670><h668>2.748"\
    "</h668><h666>2.647</h666><h664>1.858</h664><h662>0.250</h662><h660>0.262</h660><h658>1.572</h658><h656>0.249"\
    "</h656><h654>0.264</h654><h652>0.257</h652><h650>0.264</h650><h648>2.868</h648></data><data><sensor>1</sensor>"\
    "<h746>0.000</h746><h744>0.000</h744><h742>0.000</h742><h740>0.000</h740><h738>0.000</h738><h736>0.000</h736>"\
    "<h734>0.000</h734><h732>0.000</h732><h730>0.000</h730><h728>0.000</h728><h726>0.000</h726><h724>0.000</h724>"\
    "<h722>0.000</h722><h720>0.000</h720><h718>0.000</h718><h716>0.000</h716><h714>0.000</h714><h712>0.000</h712>"\
    "<h710>0.000</h710><h708>0.000</h708><h706>0.000</h706><h704>0.000</h704><h702>0.000</h702><h700>0.000</h700>"\
    "<h698>0.000</h698><h696>0.000</h696><h694>0.000</h694><h692>0.000</h692><h690>0.000</h690><h688>0.000</h688>"\
    "<h686>0.000</h686><h684>0.000</h684><h682>0.000</h682><h680>0.000</h680><h678>0.000</h678><h676>0.000</h676>"\
    "<h674>0.000</h674><h672>0.000</h672><h670>0.000</h670><h668>0.000</h668><h666>0.000</h666><h664>0.000</h664>"\
    "<h662>0.000</h662><h660>0.000</h660><h658>0.000</h658><h656>0.000</h656><h654>0.000</h654><h652>0.000</h652>"\
    "<h650>0.000</h650><h648>0.000</h648></data><data><sensor>2</sensor><h746>0.000</h746><h744>0.000</h744><h742>"\
    "0.000</h742><h740>0.000</h740><h738>0.000</h738><h736>0.000</h736><h734>0.000</h734><h732>0.000</h732><h730>"\
    "0.000</h730><h728>0.000</h728><h726>0.000</h726><h724>0.000</h724><h722>0.000</h722><h720>0.000</h720><h718>"\
    "0.000</h718><h716>0.000</h716><h714>0.000</h714><h712>0.000</h712><h710>0.000</h710><h708>0.000</h708><h706>"\
    "0.000</h706><h704>0.000</h704><h702>0.000</h702><h700>0.000</h700><h698>0.000</h698><h696>0.000</h696><h694>"\
    "0.000</h694><h692>0.000</h692><h690>0.000</h690><h688>0.000</h688><h686>0.000</h686><h684>0.000</h684><h682>"\
    "0.000</h682><h680>0.000</h680><h678>0.000</h678><h676>0.000</h676><h674>0.000</h674><h672>0.000</h672><h670>"\
    "0.000</h670><h668>0.000</h668><h666>0.000</h666><h664>0.000</h664><h662>0.000</h662><h660>0.000</h660><h658>"\
    "0.000</h658><h656>0.000</h656><h654>0.000</h654><h652>0.000</h652><h650>0.000</h650><h648>0.000</h648></data>"\
    "<data><sensor>3</sensor><h746>0.000</h746><h744>0.000</h744><h742>0.000</h742><h740>0.000</h740><h738>0.000"\
    "</h738><h736>0.000</h736><h734>0.000</h734><h732>0.000</h732><h730>0.000</h730><h728>0.000</h728><h726>0.000"\
    "</h726><h724>0.000</h724><h722>0.000</h722><h720>0.000</h720><h718>0.000</h718><h716>0.000</h716><h714>0.000"\
    "</h714><h712>0.000</h712><h710>0.000</h710><h708>0.000</h708><h706>0.000</h706><h704>0.000</h704><h702>0.000"\
    "</h702><h700>0.000</h700><h698>0.000</h698><h696>0.000</h696><h694>0.000</h694><h692>0.000</h692><h690>0.000"\
    "</h690><h688>0.000</h688><h686>0.000</h686><h684>0.000</h684><h682>0.000</h682><h680>0.000</h680><h678>0.000"\
    "</h678><h676>0.000</h676><h674>0.000</h674><h672>0.000</h672><h670>0.000</h670><h668>0.000</h668><h666>0.000"\
    "</h666><h664>0.000</h664><h662>0.000</h662><h660>0.000</h660><h658>0.000</h658><h656>0.000</h656><h654>0.000"\
    "</h654><h652>0.000</h652><h650>0.000</h650><h648>0.000</h648></data><data><sensor>4</sensor><h746>0.000</h746>"\
    "<h744>0.000</h744><h742>0.000</h742><h740>0.000</h740><h738>0.000</h738><h736>0.000</h736><h734>0.000</h734>"\
    "<h732>0.000</h732><h730>0.000</h730><h728>0.000</h728><h726>0.000</h726><h724>0.000</h724><h722>0.000</h722>"\
    "<h720>0.000</h720><h718>0.000</h718><h716>0.000</h716><h714>0.000</h714><h712>0.000</h712><h710>0.000</h710>"\
    "<h708>0.000</h708><h706>0.000</h706><h704>0.000</h704><h702>0.000</h702><h700>0.000</h700><h698>0.000</h698>"\
    "<h696>0.000</h696><h694>0.000</h694><h692>0.000</h692><h690>0.000</h690><h688>0.000</h688><h686>0.000</h686>"\
    "<h684>0.000</h684><h682>0.000</h682><h680>0.000</h680><h678>0.000</h678><h676>0.000</h676><h674>0.000</h674>"\
    "<h672>0.000</h672><h670>0.000</h670><h668>0.000</h668><h666>0.000</h666><h664>0.000</h664><h662>0.000</h662>"\
    "<h660>0.000</h660><h658>0.000</h658><h656>0.000</h656><h654>0.000</h654><h652>0.000</h652><h650>0.000</h650>"\
    "<h648>0.000</h648></data><data><sensor>5</sensor><h746>0.000</h746><h744>0.000</h744><h742>0.000</h742><h740>"\
    "0.000</h740><h738>0.000</h738><h736>0.000</h736><h734>0.000</h734><h732>0.000</h732><h730>0.000</h730><h728>"\
    "0.000</h728><h726>0.000</h726><h724>0.000</h724><h722>0.000</h722><h720>0.000</h720><h718>0.000</h718><h716>"\
    "0.000</h716><h714>0.000</h714><h712>0.000</h712><h710>0.000</h710><h708>0.000</h708><h706>0.000</h706><h704>"\
    "0.000</h704><h702>0.000</h702><h700>0.000</h700><h698>0.000</h698><h696>0.000</h696><h694>0.000</h694><h692>"\
    "0.000</h692><h690>0.000</h690><h688>0.000</h688><h686>0.000</h686><h684>0.000</h684><h682>0.000</h682><h680>"\
    "0.000</h680><h678>0.000</h678><h676>0.000</h676><h674>0.000</h674><h672>0.000</h672><h670>0.000</h670><h668>"\
    "0.000</h668><h666>0.000</h666><h664>0.000</h664><h662>0.000</h662><h660>0.000</h660><h658>0.000</h658><h656>"\
    "0.000</h656><h654>0.000</h654><h652>0.000</h652><h650>0.000</h650><h648>0.000</h648></data><data><sensor>6"\
    "</sensor><h746>0.000</h746><h744>0.000</h744><h742>0.000</h742><h740>0.000</h740><h738>0.000</h738><h736>"\
    "0.000</h736><h734>0.000</h734><h732>0.000</h732><h730>0.000</h730><h728>0.000</h728><h726>0.000</h726><h724>"\
    "0.000</h724><h722>0.000</h722><h720>0.000</h720><h718>0.000</h718><h716>0.000</h716><h714>0.000</h714><h712>"\
    "0.000</h712><h710>0.000</h710><h708>0.000</h708><h706>0.000</h706><h704>0.000</h704><h702>0.000</h702><h700>"\
    "0.000</h700><h698>0.000</h698><h696>0.000</h696><h694>0.000</h694><h692>0.000</h692><h690>0.000</h690><h688>"\
    "0.000</h688><h686>0.000</h686><h684>0.000</h684><h682>0.000</h682><h680>0.000</h680><h678>0.000</h678><h676>"\
    "0.000</h676><h674>0.000</h674><h672>0.000</h672><h670>0.000</h670><h668>0.000</h668><h666>0.000</h666><h664>"\
    "0.000</h664><h662>0.000</h662><h660>0.000</h660><h658>0.000</h658><h656>0.000</h656><h654>0.000</h654><h652>"\
    "0.000</h652><h650>0.000</h650><h648>0.000</h648></data><data><sensor>7</sensor><h746>0.000</h746><h744>0.000"\
    "</h744><h742>0.000</h742><h740>0.000</h740><h738>0.000</h738><h736>0.000</h736><h734>0.000</h734><h732>0.000"\
    "</h732><h730>0.000</h730><h728>0.000</h728><h726>0.000</h726><h724>0.000</h724><h722>0.000</h722><h720>0.000"\
    "</h720><h718>0.000</h718><h716>0.000</h716><h714>0.000</h714><h712>0.000</h712><h710>0.000</h710><h708>0.000"\
    "</h708><h706>0.000</h706><h704>0.000</h704><h702>0.000</h702><h700>0.000</h700><h698>0.000</h698><h696>0.000"\
    "</h696><h694>0.000</h694><h692>0.000</h692><h690>0.000</h690><h688>0.000</h688><h686>0.000</h686><h684>0.000"\
    "</h684><h682>0.000</h682><h680>0.000</h680><h678>0.000</h678><h676>0.000</h676><h674>0.000</h674><h672>0.000"\
    "</h672><h670>0.000</h670><h668>0.000</h668><h666>0.000</h666><h664>0.000</h664><h662>0.000</h662><h660>0.000"\
    "</h660><h658>0.000</h658><h656>0.000</h656><h654>0.000</h654><h652>0.000</h652><h650>0.000</h650><h648>0.000"\
    "</h648></data><data><sensor>8</sensor><h746>0.000</h746><h744>0.000</h744><h742>0.000</h742><h740>0.000</h740>"\
    "<h738>0.000</h738><h736>0.000</h736><h734>0.000</h734><h732>0.000</h732><h730>0.000</h730><h728>0.000</h728>"\
    "<h726>0.000</h726><h724>0.000</h724><h722>0.000</h722><h720>0.000</h720><h718>0.000</h718><h716>0.000</h716>"\
    "<h714>0.000</h714><h712>0.000</h712><h710>0.000</h710><h708>0.000</h708><h706>0.000</h706><h704>0.000</h704>"\
    "<h702>0.000</h702><h700>0.000</h700><h698>0.000</h698><h696>0.000</h696><h694>0.000</h694><h692>0.000</h692>"\
    "<h690>0.000</h690><h688>0.000</h688><h686>0.000</h686><h684>0.000</h684><h682>0.000</h682><h680>0.000</h680>"\
    "<h678>0.000</h678><h676>0.000</h676><h674>0.000</h674><h672>0.000</h672><h670>0.000</h670><h668>0.000</h668>"\
    "<h666>0.000</h666><h664>0.000</h664><h662>0.000</h662><h660>0.000</h660><h658>0.000</h658><h656>0.000</h656>"\
    "<h654>0.000</h654><h652>0.000</h652><h650>0.000</h650><h648>0.000</h648></data><data><sensor>9</sensor><h746>"\
    "0.000</h746><h744>0.000</h744><h742>0.000</h742><h740>0.000</h740><h738>0.000</h738><h736>0.000</h736><h734>"\
    "0.000</h734><h732>0.000</h732><h730>0.000</h730><h728>0.000</h728><h726>0.000</h726><h724>0.000</h724><h722>"\
    "0.000</h722><h720>0.000</h720><h718>0.000</h718><h716>0.000</h716><h714>0.000</h714><h712>0.000</h712><h710>"\
    "0.000</h710><h708>0.000</h708><h706>0.000</h706><h704>0.000</h704><h702>0.000</h702><h700>0.000</h700><h698>"\
    "0.000</h698><h696>0.000</h696><h694>0.000</h694><h692>0.000</h692><h690>0.000</h690><h688>0.000</h688><h686>"\
    "0.000</h686><h684>0.000</h684><h682>0.000</h682><h680>0.000</h680><h678>0.000</h678><h676>0.000</h676><h674>"\
    "0.000</h674><h672>0.000</h672><h670>0.000</h670><h668>0.000</h668><h666>0.000</h666><h664>0.000</h664><h662>"\
    "0.000</h662><h660>0.000</h660><h658>0.000</h658><h656>0.000</h656><h654>0.000</h654><h652>0.000</h652><h650>"\
    "0.000</h650><h648>0.000</h648></data></hist></msg>"


class SocatMessager(Thread):
    """Thread that send message over Socat."""

    def __init__(self, context, port, message=None):
        """Constructor"""
        Thread.__init__(self)
        self.context = context
        self.port = port
        self.message = message

    def run(self):
        """Main method."""
        sleep(4)
        if self.message is not None:
            ser = serial.Serial(self.port, BAUDS)
            ser.write(bytes("%s\n" % self.message, "utf-8"))
            sleep(1)
            ser.close()
        else:
            try:
                sleep(3)
                os.killpg(self.context.socat.pid, signal.SIGTERM)
                sleep(1)
            except AttributeError:
                pass


def command_currentcost_parameters(setting_type):
    """Return accordign parameter
    """
    ch1 = None
    ch1_kwh = None
    ch2 = None
    ch2_kwh = None
    ch3 = None
    ch3_kwh = None
    tmpr = None
    tty_port = TEST_CC_CORRECT_TTY_PORT
    timeout = 10
    array_instant_conso = [
        CC_INSTANT_CONSO_1_TS_3,
        CC_INSTANT_CONSO_2_TS_3,
        CC_INSTANT_CONSO_2_TS_7,
        CC_INSTANT_CONSO_3_TS_3]
    if setting_type in ERROR_CC_BAD_PORT:
        tty_port = TEST_CC_BAD_TTY_PORT
    if setting_type in ERROR_CC_NO_MESSAGE:
        timeout = 1
    if setting_type in array_instant_conso:
        ch1 = TEST_CC_VARIABLE_ID_WATTS_CH1
        ch1_kwh = TEST_CC_VARIABLE_ID_KWH_CH1
        tmpr = TEST_CC_VARIABLE_ID_TMPR
    if setting_type in CC_INSTANT_CONSO_2_TS_7:
        ch2 = TEST_CC_VARIABLE_ID_WATTS_CH2
        ch2_kwh = TEST_CC_VARIABLE_ID_KWH_CH2
        ch3 = TEST_CC_VARIABLE_ID_WATTS_CH3
        ch3_kwh = TEST_CC_VARIABLE_ID_KWH_CH3

    return {
        "tty_port": tty_port,
        "timeout": timeout,
        "usb_retry": 5,
        "ch1": ch1,
        "ch2": ch2,
        "ch3": ch3,
        "ch1_kwh": ch1_kwh,
        "ch2_kwh": ch2_kwh,
        "ch3_kwh": ch3_kwh,
        "tmpr": tmpr
    }


def command_currencost_errors(setting_type, context, cc_params):
    """Return according errors
    """
    error = None
    if setting_type in ERROR_CC_BAD_PORT:
        error = (TEST_CC_VARIABLE_ID, context.site_id, cc_params["tty_port"], cc_params["usb_retry"])
    elif setting_type in ERROR_CC_NO_MESSAGE:
        error = (TEST_CC_VARIABLE_ID, context.site_id)
    elif setting_type in ERROR_CC_DISCONNECTED:
        error = (TEST_CC_VARIABLE_ID, context.site_id, cc_params["tty_port"])
    elif setting_type in ERROR_CC_INCORRECT_MESSAGE:
        error = (TEST_CC_VARIABLE_ID, context.site_id, WRONG_CURRENTCOST_MESSAGE)
    elif setting_type in ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR:
        error = (TEST_CC_VARIABLE_ID, context.site_id, INCORRECT_TMPR_CURRENTCOST_MESSAGE)
    elif setting_type in ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS:
        error = (TEST_CC_VARIABLE_ID, context.site_id, INCORRECT_WATTS_CURRENTCOST_MESSAGE)
    return error


def command_currencost_thread(setting_type, context, tty_port):
    """Returning according thread
    """
    thread = None
    if setting_type in ERROR_CC_DISCONNECTED:
        thread = SocatMessager(context, tty_port)
    elif setting_type in ERROR_CC_INCORRECT_MESSAGE:
        thread = SocatMessager(context, tty_port, WRONG_CURRENTCOST_MESSAGE)
    elif setting_type in ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR:
        thread = SocatMessager(context, tty_port, INCORRECT_TMPR_CURRENTCOST_MESSAGE)
    elif setting_type in ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS:
        thread = SocatMessager(context, tty_port, INCORRECT_WATTS_CURRENTCOST_MESSAGE)
    elif setting_type in [CC_INSTANT_CONSO_1_TS_0, CC_INSTANT_CONSO_1_TS_3]:
        thread = SocatMessager(context, tty_port, CURRENTCOST_MESSAGE)
    elif setting_type in [CC_INSTANT_CONSO_2_TS_3, CC_INSTANT_CONSO_2_TS_0, CC_INSTANT_CONSO_2_TS_7]:
        thread = SocatMessager(context, tty_port, CURRENTCOST_MESSAGE_2)
    elif setting_type in CC_INSTANT_CONSO_3_TS_3:
        thread = SocatMessager(context, tty_port, CURRENTCOST_MESSAGE_3)
    elif setting_type in CC_HISTORY:
        thread = SocatMessager(context, tty_port, HISTORY_1)
    return thread


def launch_currentcost_command(out, context, setting_type):
    """Launch CurrentCost command
    """
    commands = "%s PTY,link=%s PTY,link=%s" % (SOCAT, TEST_CC_CORRECT_TTY_PORT, TEST_CC_CORRECT_TTY_PORT_WRITER)
    context.socat = subprocess.Popen(shlex.split(commands), stdout=subprocess.PIPE, preexec_fn=os.setsid)
    cc_params = command_currentcost_parameters(setting_type)
    error = command_currencost_errors(setting_type, context, cc_params)
    if error is not None:
        context.specific_error = error
    thread = command_currencost_thread(setting_type, context, TEST_CC_CORRECT_TTY_PORT_WRITER)
    if thread is not None:
        context.thread = thread
        context.thread.start()
    command = CurrentCostCommand()
    command.out = out
    sleep(3)
    command.handle(
        site_id=context.site_id,
        variable_id=TEST_CC_VARIABLE_ID,
        tty_port=cc_params["tty_port"],
        timeout=cc_params["timeout"],
        usb_retry=cc_params["usb_retry"],
        break_loop=True,
        ch1=cc_params["ch1"],
        ch1_kwh=cc_params["ch1_kwh"],
        ch2=cc_params["ch2"],
        ch2_kwh=cc_params["ch2_kwh"],
        ch3=cc_params["ch3"],
        ch3_kwh=cc_params["ch3_kwh"],
        tmpr=cc_params["tmpr"])


def verify_currentcost_data(variable, variable_id, data_type):
    """Verify currentcost data
    """
    assert_equal(variable.start_value, DICT_CC_INSTANT_CONSO[variable_id][data_type][KEY_START_VALUE])
    if KEY_END_VALUE_2 in DICT_CC_INSTANT_CONSO[variable_id][data_type]:
        assert_gte(variable.end_value, DICT_CC_INSTANT_CONSO[variable_id][data_type][KEY_END_VALUE])
        assert_lte(variable.end_value, DICT_CC_INSTANT_CONSO[variable_id][data_type][KEY_END_VALUE_2])
    else:
        assert_equal(variable.end_value, DICT_CC_INSTANT_CONSO[variable_id][data_type][KEY_END_VALUE])


def verify_currentcost_data_update(site_id, data_type):
    """Verify currentcost data update
    """
    site = get_site_by_slug(slug=site_id)
    if site is None:
        assert_equal("Site %s does not exist" % site_id, False)

    for variable_id in DICT_CC_INSTANT_CONSO:
        variable = get_variable_by_slug(site=site, slug=variable_id)
        if variable is not None:
            verify_currentcost_data(variable, variable_id, data_type)
        else:
            if data_type not in CC_INSTANT_CONSO_1_TS_0:
                assert_equal("Variable %s does not exist" % variable_id, False)


def verify_currentcost_tsv_update(site_id, data_type):
    """Verify currentcost TSV update
    """
    for variable_id in DICT_CC_INSTANT_CONSO:
        last_series = FILE_STORAGE_SPACE.get_last_series(site_id, variable_id)
        if data_type in CC_INSTANT_CONSO_1_TS_0:
            assert_equal(last_series, None)
        else:
            last_series_value = last_series[KEY_VALUE]
            expected_value_1 = DICT_CC_INSTANT_CONSO[variable_id][data_type][KEY_END_VALUE]
            if KEY_END_VALUE_2 in DICT_CC_INSTANT_CONSO[variable_id][data_type]:
                expected_value_2 = DICT_CC_INSTANT_CONSO[variable_id][data_type][KEY_END_VALUE_2]
                assert_gte(last_series_value, expected_value_1)
                assert_lte(last_series_value, expected_value_2)
            else:
                assert_equal(last_series_value, expected_value_1)
            assert_equal(last_series[KEY_SITE_ID], site_id)
            assert_equal(last_series[KEY_VARIABLE_ID], variable_id)
