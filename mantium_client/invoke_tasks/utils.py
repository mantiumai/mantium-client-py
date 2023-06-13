"""Monkeypatch for getting annotations to work with Invoke tasks."""
import sys
from inspect import ArgSpec, getfullargspec
from typing import Any, Callable
from unittest.mock import patch

import invoke


def fix_annotations() -> None:
    """Pyinvoke doesnt accept annotations by default, this fixes that.

    Based on: https://github.com/pyinvoke/invoke/pull/606
    """

    def patched_inspect_getargspec(func: Callable) -> ArgSpec:
        """Patch inspect.getargspec to use inspect.getfullargspec."""
        spec = getfullargspec(func)
        return ArgSpec(*spec[0:4])  # type: ignore

    org_task_argspec = invoke.tasks.Task.argspec

    def patched_task_argspec(*args: Any, **kwargs: Any) -> ArgSpec:
        """Patch invoke.tasks.Task.argspec to use patched_inspect_getargspec."""
        with patch(target='inspect.getargspec', new=patched_inspect_getargspec):
            return org_task_argspec(*args, **kwargs)

    invoke.tasks.Task.argspec = patched_task_argspec    # type: ignore


def get_base_prefix_compat() -> str:
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, 'base_prefix', None) or getattr(sys, 'real_prefix', None) or sys.prefix


def in_virtualenv() -> bool:
    """Check if you're in a virtualenv"""
    return get_base_prefix_compat() != sys.prefix
