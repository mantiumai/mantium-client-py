# This MUST be called prior to importing any of the invoke commands
# It fixes the issue outlined here: https://github.com/pyinvoke/invoke/issues/357
from inspect import ArgSpec, getfullargspec
from typing import Any, Callable
from unittest.mock import patch

import invoke


def fix_annotations() -> None:
    """Pyinvoke doesnt accept annotations by default, this fix that.

    Based on: https://github.com/pyinvoke/invoke/pull/606
    """

    def patched_inspect_getargspec(func: Callable) -> ArgSpec:
        spec = getfullargspec(func)
        return ArgSpec(*spec[0:4])

    org_task_argspec = invoke.tasks.Task.argspec

    def patched_task_argspec(*args: Any, **kwargs: Any):
        with patch(target='inspect.getargspec', new=patched_inspect_getargspec):
            return org_task_argspec(*args, **kwargs)

    invoke.tasks.Task.argspec = patched_task_argspec


fix_annotations()
