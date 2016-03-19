#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for CurrentCost"""

import os
import shlex
import signal
import serial
import subprocess
from time import sleep
from threading import Thread
from timevortex.models import get_site_by_slug, get_variable_by_slug
from timevortex.utils.filestorage import FILE_STORAGE_SPACE
from timevortex.utils.globals import KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE
from features.steps.test_globals import SOCAT, assertEqual, assertGTE, assertLTE
from energy.management.commands.retrieve_currentcost_data import Command as CurrentCostCommand
from energy.utils.globals import ERROR_CC_BAD_PORT, ERROR_CC_DISCONNECTED, ERROR_CC_NO_MESSAGE
from energy.utils.globals import ERROR_CC_INCORRECT_MESSAGE, ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR
from energy.utils.globals import ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS


TIMEVORTEX_CURRENTCOST_LOG_FILE = "/tmp/timevortex_energy.log"
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
DICT_CC_INSTANT_CONSO = {
    CC_INSTANT_CONSO_1_TS_0: {
        TEST_CC_VARIABLE_ID_WATTS_CH1: {
            KEY_START_VALUE: None,
            KEY_END_VALUE: None
        },
        TEST_CC_VARIABLE_ID_KWH_CH1: {
            KEY_START_VALUE: None,
            KEY_END_VALUE: None
        },
        TEST_CC_VARIABLE_ID_WATTS_CH2: {
            KEY_START_VALUE: None,
            KEY_END_VALUE: None
        },
        TEST_CC_VARIABLE_ID_KWH_CH2: {
            KEY_START_VALUE: None,
            KEY_END_VALUE: None
        },
        TEST_CC_VARIABLE_ID_WATTS_CH3: {
            KEY_START_VALUE: None,
            KEY_END_VALUE: None
        },
        TEST_CC_VARIABLE_ID_KWH_CH3: {
            KEY_START_VALUE: None,
            KEY_END_VALUE: None
        },
        TEST_CC_VARIABLE_ID_TMPR: {
            KEY_START_VALUE: None,
            KEY_END_VALUE: None
        }
    },
    CC_INSTANT_CONSO_2_TS_7: {
        TEST_CC_VARIABLE_ID_WATTS_CH1: {
            KEY_START_VALUE: "406.0",
            KEY_END_VALUE: "406.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH1: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_WATTS_CH2: {
            KEY_START_VALUE: "14405.0",
            KEY_END_VALUE: "14405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH2: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_WATTS_CH3: {
            KEY_START_VALUE: "10405.0",
            KEY_END_VALUE: "10405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH3: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_TMPR: {
            KEY_START_VALUE: "20.3",
            KEY_END_VALUE: "20.3"
        }
    },
    CC_INSTANT_CONSO_1_TS_3: {
        TEST_CC_VARIABLE_ID_WATTS_CH1: {
            KEY_START_VALUE: "406.0",
            KEY_END_VALUE: "405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH1: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0003",
            KEY_END_VALUE_2: "0.0004",
        },
        TEST_CC_VARIABLE_ID_WATTS_CH2: {
            KEY_START_VALUE: "14405.0",
            KEY_END_VALUE: "14405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH2: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_WATTS_CH3: {
            KEY_START_VALUE: "10405.0",
            KEY_END_VALUE: "10405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH3: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_TMPR: {
            KEY_START_VALUE: "20.3",
            KEY_END_VALUE: "19.3"
        }
    },
    CC_INSTANT_CONSO_2_TS_3: {
        TEST_CC_VARIABLE_ID_WATTS_CH1: {
            KEY_START_VALUE: "406.0",
            KEY_END_VALUE: "406.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH1: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.00065",
            KEY_END_VALUE_2: "0.00075"
        },
        TEST_CC_VARIABLE_ID_WATTS_CH2: {
            KEY_START_VALUE: "14405.0",
            KEY_END_VALUE: "14405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH2: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_WATTS_CH3: {
            KEY_START_VALUE: "10405.0",
            KEY_END_VALUE: "10405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH3: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_TMPR: {
            KEY_START_VALUE: "20.3",
            KEY_END_VALUE: "20.3"
        }
    },
    CC_INSTANT_CONSO_2_TS_0: {
        TEST_CC_VARIABLE_ID_WATTS_CH1: {
            KEY_START_VALUE: "406.0",
            KEY_END_VALUE: "406.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH1: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.00065",
            KEY_END_VALUE_2: "0.00075"
        },
        TEST_CC_VARIABLE_ID_WATTS_CH2: {
            KEY_START_VALUE: "14405.0",
            KEY_END_VALUE: "14405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH2: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_WATTS_CH3: {
            KEY_START_VALUE: "10405.0",
            KEY_END_VALUE: "10405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH3: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_TMPR: {
            KEY_START_VALUE: "20.3",
            KEY_END_VALUE: "20.3"
        }
    },
    CC_INSTANT_CONSO_3_TS_3: {
        TEST_CC_VARIABLE_ID_WATTS_CH1: {
            KEY_START_VALUE: "406.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH1: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0013",
            KEY_END_VALUE_2: "0.0014"
        },
        TEST_CC_VARIABLE_ID_WATTS_CH2: {
            KEY_START_VALUE: "14405.0",
            KEY_END_VALUE: "14405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH2: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_WATTS_CH3: {
            KEY_START_VALUE: "10405.0",
            KEY_END_VALUE: "10405.0"
        },
        TEST_CC_VARIABLE_ID_KWH_CH3: {
            KEY_START_VALUE: "0.0",
            KEY_END_VALUE: "0.0"
        },
        TEST_CC_VARIABLE_ID_TMPR: {
            KEY_START_VALUE: "20.3",
            KEY_END_VALUE: "21.3"
        }
    },
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
        sleep(1)

        if self.message is not None:
            ser = serial.Serial(self.port)
            ser.write(bytes("%s\n" % self.message, "utf-8"))
            sleep(1)
            ser.close()
        else:
            try:
                os.killpg(self.context.socat.pid, signal.SIGTERM)
                sleep(1)
            except AttributeError:
                pass


def launch_currentcost_command(out, context, setting_type):
    commands = "%s PTY,link=%s PTY,link=%s" % (SOCAT, TEST_CC_CORRECT_TTY_PORT, TEST_CC_CORRECT_TTY_PORT_WRITER)
    context.socat = subprocess.Popen(shlex.split(commands), stdout=subprocess.PIPE, preexec_fn=os.setsid)
    tty_port = TEST_CC_CORRECT_TTY_PORT
    timeout = 10
    usb_retry = 1
    ch1 = None
    ch2 = None
    ch3 = None
    ch1_kwh = None
    ch2_kwh = None
    ch3_kwh = None
    tmpr = None
    command = CurrentCostCommand()
    command.out = out
    if setting_type in ERROR_CC_BAD_PORT:
        tty_port = TEST_CC_BAD_TTY_PORT
        context.specific_error = (TEST_CC_VARIABLE_ID, context.site_id, tty_port, usb_retry)
    elif setting_type in ERROR_CC_NO_MESSAGE:
        timeout = 1
        context.specific_error = (TEST_CC_VARIABLE_ID, context.site_id)
    elif setting_type in ERROR_CC_DISCONNECTED:
        context.thread = SocatMessager(context, tty_port)
        context.thread.start()
        context.specific_error = (TEST_CC_VARIABLE_ID, context.site_id, tty_port)
    elif setting_type in ERROR_CC_INCORRECT_MESSAGE:
        context.thread = SocatMessager(context, tty_port, WRONG_CURRENTCOST_MESSAGE)
        context.thread.start()
        context.specific_error = (TEST_CC_VARIABLE_ID, context.site_id, WRONG_CURRENTCOST_MESSAGE)
    elif setting_type in ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR:
        context.thread = SocatMessager(context, tty_port, INCORRECT_TMPR_CURRENTCOST_MESSAGE)
        context.thread.start()
        context.specific_error = (TEST_CC_VARIABLE_ID, context.site_id, INCORRECT_TMPR_CURRENTCOST_MESSAGE)
    elif setting_type in ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS:
        context.thread = SocatMessager(context, tty_port, INCORRECT_WATTS_CURRENTCOST_MESSAGE)
        context.thread.start()
        context.specific_error = (TEST_CC_VARIABLE_ID, context.site_id, INCORRECT_WATTS_CURRENTCOST_MESSAGE)
    elif setting_type in CC_INSTANT_CONSO_1_TS_0:
        context.thread = SocatMessager(context, tty_port, CURRENTCOST_MESSAGE)
        context.thread.start()
    elif setting_type in CC_INSTANT_CONSO_1_TS_3:
        ch1 = TEST_CC_VARIABLE_ID_WATTS_CH1
        ch1_kwh = TEST_CC_VARIABLE_ID_KWH_CH1
        tmpr = TEST_CC_VARIABLE_ID_TMPR
        context.thread = SocatMessager(context, tty_port, CURRENTCOST_MESSAGE)
        context.thread.start()
    elif setting_type in CC_INSTANT_CONSO_2_TS_3:
        ch1 = TEST_CC_VARIABLE_ID_WATTS_CH1
        ch1_kwh = TEST_CC_VARIABLE_ID_KWH_CH1
        tmpr = TEST_CC_VARIABLE_ID_TMPR
        context.thread = SocatMessager(context, tty_port, CURRENTCOST_MESSAGE_2)
        context.thread.start()
    elif setting_type in CC_INSTANT_CONSO_2_TS_0:
        context.thread = SocatMessager(context, tty_port, CURRENTCOST_MESSAGE_2)
        context.thread.start()
    elif setting_type in CC_INSTANT_CONSO_2_TS_7:
        ch1 = TEST_CC_VARIABLE_ID_WATTS_CH1
        ch1_kwh = TEST_CC_VARIABLE_ID_KWH_CH1
        ch2 = TEST_CC_VARIABLE_ID_WATTS_CH2
        ch2_kwh = TEST_CC_VARIABLE_ID_KWH_CH2
        ch3 = TEST_CC_VARIABLE_ID_WATTS_CH3
        ch3_kwh = TEST_CC_VARIABLE_ID_KWH_CH3
        tmpr = TEST_CC_VARIABLE_ID_TMPR
        context.thread = SocatMessager(context, tty_port, CURRENTCOST_MESSAGE_2)
        context.thread.start()
    elif setting_type in CC_INSTANT_CONSO_3_TS_3:
        ch1 = TEST_CC_VARIABLE_ID_WATTS_CH1
        ch1_kwh = TEST_CC_VARIABLE_ID_KWH_CH1
        tmpr = TEST_CC_VARIABLE_ID_TMPR
        context.thread = SocatMessager(context, tty_port, CURRENTCOST_MESSAGE_3)
        context.thread.start()
    elif setting_type in CC_HISTORY:
        context.thread = SocatMessager(context, tty_port, HISTORY_1)
        context.thread.start()
    command.handle(
        site_id=context.site_id,
        variable_id=TEST_CC_VARIABLE_ID,
        tty_port=tty_port,
        timeout=timeout,
        usb_retry=usb_retry,
        break_loop=True,
        ch1=ch1,
        ch1_kwh=ch1_kwh,
        ch2=ch2,
        ch2_kwh=ch2_kwh,
        ch3=ch3,
        ch3_kwh=ch3_kwh,
        tmpr=tmpr)


def verify_currentcost_data_update(site_id, data_type):

    site = get_site_by_slug(slug=site_id)
    if site is None:
        assertEqual("Site %s does not exist" % site_id, False)

    for variable_id in DICT_CC_INSTANT_CONSO[data_type]:
        variable = get_variable_by_slug(site=site, slug=variable_id)
        if variable is not None:
            assertEqual(variable.start_value, DICT_CC_INSTANT_CONSO[data_type][variable_id][KEY_START_VALUE])
            if KEY_END_VALUE_2 in DICT_CC_INSTANT_CONSO[data_type][variable_id]:
                assertGTE(variable.end_value, DICT_CC_INSTANT_CONSO[data_type][variable_id][KEY_END_VALUE])
                assertLTE(variable.end_value, DICT_CC_INSTANT_CONSO[data_type][variable_id][KEY_END_VALUE_2])
            else:
                assertEqual(variable.end_value, DICT_CC_INSTANT_CONSO[data_type][variable_id][KEY_END_VALUE])
        else:
            if data_type not in CC_INSTANT_CONSO_1_TS_0:
                assertEqual("Variable %s does not exist" % variable_id, False)


def verify_currentcost_tsv_update(site_id, data_type):
    for variable_id in DICT_CC_INSTANT_CONSO[data_type]:
        last_series = FILE_STORAGE_SPACE.get_last_series(site_id, variable_id)
        if data_type in CC_INSTANT_CONSO_1_TS_0:
            assertEqual(last_series, None)
        else:
            if KEY_END_VALUE_2 in DICT_CC_INSTANT_CONSO[data_type][variable_id]:
                assertGTE(last_series[KEY_VALUE], DICT_CC_INSTANT_CONSO[data_type][variable_id][KEY_END_VALUE])
                assertLTE(last_series[KEY_VALUE], DICT_CC_INSTANT_CONSO[data_type][variable_id][KEY_END_VALUE_2])
            else:
                assertEqual(last_series[KEY_VALUE], DICT_CC_INSTANT_CONSO[data_type][variable_id][KEY_END_VALUE])
            assertEqual(last_series[KEY_SITE_ID], site_id)
            assertEqual(last_series[KEY_VARIABLE_ID], variable_id)
