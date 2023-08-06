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
