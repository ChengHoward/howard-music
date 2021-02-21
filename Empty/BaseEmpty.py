import json


class BaseEmpty(object):
    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=lambda o: {_: __ for _, __ in o.__dict__.items() if __ is not None},
                          ensure_ascii=False)

    def __str__(self):
        return self.__dict__.__str__()

    def to_dict(self) -> dict:
        return json.loads(
            json.dumps(self.__dict__, default=lambda o: {_: __ for _, __ in o.__dict__.items() if __ is not None},
                       ensure_ascii=False))
