"""
"""
from __future__ import annotations

import time
from http import HTTPStatus

import gradio as gr
import requests
from pydantic import BaseModel

from .. import utils
from ..config import Config


CGROUP_PATH = utils.self_cgroup_device_path()
TOKEN_HEADER = 'X-IP-Token'


class ScheduleParams(BaseModel):
    cgroupPath: str
    taskId: int
    token: str

class ScheduleResponse(BaseModel):
    idle: bool
    nvidiaIndex: int
    nvidiaUUID: str

class ReleaseParams(BaseModel):
    cgroupPath: str
    taskId: int
    nvidiaIndex: int
    fail: bool


def base_url() -> str:
    assert Config.zero_device_api_url is not None
    return Config.zero_device_api_url


def post(path: str, params: BaseModel | None = None) -> requests.Response:
    return requests.post(base_url() + path, params=params.dict() if params else None)


def startup_report():
    retries, max_retries = 0, 2
    while (status := post('/startup-report').status_code) == HTTPStatus.NOT_FOUND: # pragma: no cover
        time.sleep(1)
        if (retries := retries + 1) > max_retries:
            raise RuntimeError("Error while initializing ZeroGPU: NotFound")
    if status != HTTPStatus.OK: # pragma: no cover
        raise RuntimeError("Error while initializing ZeroGPU: Unknown")


def schedule(task_id: int, request: gr.Request) -> ScheduleResponse:

    if not hasattr(request, 'headers') or not hasattr(request.headers, '__dict__'):
        raise gr.Error("Internal Gradio error")

    if not (token := request.headers.__dict__.get(TOKEN_HEADER.lower())):
        raise gr.Error("Internal infra error")

    res = post('/schedule', params=ScheduleParams(
        cgroupPath=CGROUP_PATH,
        taskId=task_id,
        token=token,
    ))

    if res.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        raise gr.Error("No GPU is currently available")

    try:
        data = res.json()
    except requests.JSONDecodeError: # pragma: no cover
        data = {}

    if not res.ok: # pragma: no cover
        raise RuntimeError(f"ZeroGPU API /schedule error: {data.get('detail')}")

    return ScheduleResponse(**data)


def release(task_id: int, nvidia_index: int, fail: bool = False) -> None:

    res = post('/release', params=ReleaseParams(
        cgroupPath=CGROUP_PATH,
        taskId=task_id,
        nvidiaIndex=nvidia_index,
        fail=fail,
    ))

    if not res.ok:
        try:
            data = res.json()
        except requests.JSONDecodeError: # pragma: no cover
            data = {}
        # TODO: use future gr.Warning() if /release didn't detect GPU usage
        raise RuntimeError(f"ZeroGPU API /release error: {data.get('detail')}")

    return None
