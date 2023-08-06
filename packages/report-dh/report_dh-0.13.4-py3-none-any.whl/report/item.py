import pytest
from ._internal import Launch
import functools
from typing import Any, Optional, Union, Literal
from .core import *
import traceback


__all__ = ['step', 'title', 'story', 'feature', 'log', 'attachment']

@pytest.fixture(scope="session", autouse=True)
def check_collection_phase(request):
    return request.config.getoption("--collect-only")
    

class step:
    def __init__(self, name: str = None):
        self.name = name

    def __call__(self, func):
        __tracebackhide__ = True
        if self.name is None:
            self.name = func.__name__

        func.__new_name__ = self.name if self.name else func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            __tracebackhide__ = True
            with self:
                return _run_func(func, *args, **kwargs)

        return wrapper

    def __enter__(self):
        __tracebackhide__ = True
        if self.name is None:
            raise ValueError("The 'name' parameter is required when using 'step' as a context manager.")

        parent = Launch.get_latest_item()
        item_id = Launch.create_report_item(
                name=self.name,
                parent_item=parent,
                type='step',
                has_stats=False,
                description='')

        Launch.add_item(self.name, item_id)

    def __exit__(self, exc_type, exc_value, tb):
        __tracebackhide__ = True

        passed = exc_type is None
        if passed:
            Launch.finish_item(self.name, passed)

        elif not passed:
            traceback_str = ''.join(traceback.format_tb(tb))
            message = f'{exc_type.__name__}: {exc_value}'
            Launch.finish_failed_item(self.name, message=message, reason=traceback_str)


class title:
    def __init__(self, name: Optional[str] = None, link: Optional[str] = None):
        self.name = name
        self.link = link

    def __call__(self, func):
        __tracebackhide__ = True
        func.__new_name__ = self.name if self.name else func.__name__
        func.__link__ = self.link
        self.__name__ = func.__name__
        self.__qualname__ = func.__qualname__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            __tracebackhide__ = True

            func.formatted_name = self.name.format(*args, **kwargs)
            self.formatted_name = self.name.format(*args, **kwargs)
            result = _run_func(func, *args, **kwargs)
            return result

        return wrapper

    def __enter__(self):
        __tracebackhide__ = True
        if self.name is None:
            raise ValueError("The 'name' parameter is required when using 'title' as a context manager.")

        parent = Launch.get_caller_name()
        item_name = getattr(self, 'formatted_name', 'name')
        item_id = Launch.create_report_item(
                name=item_name,
                parent_item=parent,
                type='scenario',
                has_stats=True,
                description='')

        Launch.add_item(self.name, item_id)

    def __exit__(self, exc_type, exc_value, tb):
        __tracebackhide__ = True
        passed = exc_type is None
        if passed:
            Launch.finish_item(self.name, passed)

        elif not passed:
            traceback_str = ''.join(traceback.format_tb(tb))
            message = f'{exc_type.__name__}: {exc_value}'
            Launch.finish_failed_item(self.name, message=message, reason=traceback_str)


def feature(name: str):
    def actual_decorator(cls):
        __tracebackhide__ = True
        cls = pytest.mark.feature(name=name, class_name=cls.__name__)(cls)
        return cls

    return actual_decorator


def story(name: str, link: Optional[str] = None):
    def actual_decorator(cls):
        cls = pytest.mark.story(name=name, class_name=cls.__name__, link=link)(cls)
        return cls

    return actual_decorator


def log(*, message: str, level: str = "INFO"):
    __tracebackhide__ = True
    item = Launch.get_caller_name()
    Launch.create_log(item=item, message=message, level=level)


def attachment(*, name: str, attachment: Union[str, bytes], item: str = '', attachment_type: str, level: Literal["ERROR", "INFO", "DEBUG"] = "ERROR"):
    """Add attachment to the item (test class/case/step)
    :param item: The item name (function name)
    :param name: The attachment name
    :param attachment: attachment as bytes or the path to the attachment
    :param attachment_type: The type of the attachment (i.e use report.attachment_type.PNG)
    :param level: The log level of the the attachment (i.e if an error occured and you want to attach a screenshot use "ERROR")
    """
    Launch.add_attachment(item=item, message=name, level=level, attachment=attachment, attachment_type=attachment_type)

