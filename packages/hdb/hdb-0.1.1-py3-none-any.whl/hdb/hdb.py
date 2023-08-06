# MIT License
#
# Copyright (c) 2023 Chris Varga
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import json


def get(location, *args, **kwargs):
    return Hobbit(location, *args, **kwargs)


class Hobbit(dict):
    def __init__(self, location, *args, **kwargs):
        super(Hobbit, self).__init__(*args, **kwargs)
        self.location = location
        self.load()

    def load(self):
        if os.path.exists(self.location):
            with open(self.location, "r") as f:
                self.update(json.load(f))

    def save(self):
        try:
            data = json.dumps(
                self,
                indent=4,
            )

        except BaseException:
            raise Exception("Data could not be encoded to json")

        with open(self.location, "w") as f:
            f.write(data)
