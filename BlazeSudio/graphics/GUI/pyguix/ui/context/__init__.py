# PyGames-pyguix
# made with: pygame 2.1.2 (SDL 2.0.16, Python 3.10.6)
# using: vscode ide
# By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay
# Copyright 2022 J. Brandon George
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os

def get_json_files():

    dirstr = __path__.__str__()
    dirstr = dirstr.rstrip("']")
    dirstr = dirstr.lstrip("['")

    jsonfiles = list()

    for root, dirs,files in os.walk(top=dirstr):
        for f in files:
            if f.__contains__(".json"):
                jsonfiles.append(f)

    return jsonfiles
