#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

import json
from sys import version_info
import requests

MIN_PYTHON_VERSION = (3, 5, 3)

_ = version_info >= MIN_PYTHON_VERSION or exit(
    "Python %d.%d.%d required" % MIN_PYTHON_VERSION
)

__version__ = "1.0.0"

###################################

class API:

    def __init__(self, name=None, pw=None):
        self._name = name
        self._pw = pw

    ### Login
    def authen(name, pw):
        print("########### begin authen ###########")    
        headers = {
            'Content-Type': 'application/json',
        }

        json_data = {
            'strUsername': name,
            'strPassword': pw,
            'strDeviceID': 'ccaf788e78517389',
        }

        response = requests.post('https://api.cskh.evnspc.vn/api/user/authenticate', headers=headers, json=json_data)

        data = response.text
        print(f"Result: {response.status_code}")
        print(data)
        print("########### done authen ###########")
        return data

########################################