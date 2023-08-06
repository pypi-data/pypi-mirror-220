"""
"""
from __future__ import annotations

import inspect
from typing import Callable
from typing import Generator
from typing import TypeVar
from typing import overload
from typing_extensions import Concatenate
from typing_extensions import ParamSpec

import gradio as gr

from ..config import Config
from . import client
from .wrappers import regular_function_wrapper
from .wrappers import generator_function_wrapper


Param = ParamSpec('Param')
Res = TypeVar('Res')


decorated_cache: dict[Callable, Callable] = {}


@overload
def GPU(
    task:
     Callable[Param, Res],
) -> Callable[Concatenate[gr.Request, Param], Res]:
    ...
@overload
def GPU(
    task:
     Callable[Param, Generator[Res, None, None]],
) -> Callable[Concatenate[gr.Request, Param], Generator[Res, None, None]]:
    ...
def GPU(
    task:
      Callable[Param, Res]
    | Callable[Param, Generator[Res, None, None]],
) -> (Callable[Concatenate[gr.Request, Param], Res]
    | Callable[Concatenate[gr.Request, Param], Generator[Res, None, None]]):
    """
    """

    if not Config.zero_gpu:
        # TODO: still prepend gr.Request for type consistency ?
        return task # type: ignore

    if task in decorated_cache:
        return decorated_cache[task] # type: ignore

    if inspect.iscoroutinefunction(task):
        raise NotImplementedError

    if inspect.isgeneratorfunction(task):
        decorated = generator_function_wrapper(task)
    else:
        decorated = regular_function_wrapper(task)

    client.startup_report()
    decorated_cache.update({
        task:      decorated,
        decorated: decorated,
    })

    return decorated # type: ignore
