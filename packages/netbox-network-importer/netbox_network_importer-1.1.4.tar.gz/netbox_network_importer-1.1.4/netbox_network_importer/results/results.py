from enum import Enum


class Status(Enum):
    CHANGED = 1
    NOT_CHANGED = 2
    FAILED = 3
    ANOMALLY = 4
    CHECK_MANUALLY = 5
    EXCEPTION = 6
    SKIPPED = 7


class Action(Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    LOOKUP = 4
    UNKNOWN = 5


class NetboxResult():
    result: str
    status: Status
    diff: dict
    action: Action
    exception: Exception

    def __init__(self, result: str, status: Status, action: Action, diff: dict, exception=None):
        self.result = result
        self.status = status
        self.diff = diff
        self.action = action
        self.exception = exception

    def to_dict(self):
        return {
            "result": self.result,
            "status": self.status.name,
            "action": self.action.name,
            "exception": self.exception,
            "diff": self.diff,
        }

    def __repr__(self):
        return self.result


class TaskNetboxResult():
    """Representation of results on Netbox though task

    :param netbox_results: list of NetboxResult
    :param task: task name
    """

    netbox_results = []  # type NetboxResult
    task = str  # task name

    def __init__(self, task: str, netbox_results: list, status, exception=None, comment=None):
        self.netbox_results = netbox_results
        self.task = task
        self.status = status
        self.exception = exception
        self.comment = comment

    def to_dict(self, except_status_codes=[]):
        """Returns dict representation of results of task action
        {
            '<task_name>': {                                                                                                      
                '<status_code>': [                                                                                                             
                    {NetboxResult.to_dict(),
                ]
        }

        :param netbox_results: list of NetboxResult
        :param except_status_codes: Does not return certain status codes
        :param task: task name
        """

        if except_status_codes:
            except_status_codes = [except_status_codes] if not isinstance(
                except_status_codes, list) else except_status_codes

        result = {self.task: {"status": self.status,
                              "comment": self.comment,
                              "results": {},
                              "exception": self.exception, }
                  }

        for res in self.netbox_results:
            if res.status in except_status_codes:
                continue

            res_dict = res.to_dict()
            if not result[self.task]['results'].get(res_dict['status'], None):
                result[self.task]['results'][res_dict['status']] = []

            result[self.task]['results'][res.status.name].append(res_dict)

        return result

    def __repr__(self):
        return self.task
