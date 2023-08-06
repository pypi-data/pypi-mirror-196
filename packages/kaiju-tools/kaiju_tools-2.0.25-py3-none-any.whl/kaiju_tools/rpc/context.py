from contextvars import ContextVar  # noqa pycharm
from typing import Union

from kaiju_tools.services import RequestContext, Session

__all__ = ['REQUEST_SESSION', 'REQUEST_CONTEXT']


REQUEST_CONTEXT: ContextVar[Union[None, RequestContext]] = ContextVar('RequestContext', default=None)
REQUEST_SESSION: ContextVar[Union[None, Session]] = ContextVar('RequestSession', default=None)
