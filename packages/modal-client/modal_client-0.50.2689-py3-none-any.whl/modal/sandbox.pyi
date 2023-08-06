import __main__
import modal.client
import modal.image
import modal.mount
import modal.object
import modal_proto.api_pb2
import typing
import typing_extensions

class _LogsReader:
    def __init__(self, file_descriptor: int, sandbox_id: str, client: modal.client._Client) -> None:
        ...

    async def read(self):
        ...


class LogsReader:
    def __init__(self, file_descriptor: int, sandbox_id: str, client: modal.client.Client) -> None:
        ...

    class __read_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    read: __read_spec


class _SandboxHandle(modal.object._Handle):
    _result: typing.Union[modal_proto.api_pb2.GenericResult, None]
    _stdout: _LogsReader
    _stderr: _LogsReader

    async def wait(self):
        ...

    @property
    def stdout(self):
        ...

    @property
    def stderr(self):
        ...


class SandboxHandle(modal.object.Handle):
    _result: typing.Union[modal_proto.api_pb2.GenericResult, None]
    _stdout: LogsReader
    _stderr: LogsReader

    def __init__(self):
        ...

    class __wait_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    wait: __wait_spec

    @property
    def stdout(self):
        ...

    @property
    def stderr(self):
        ...


class _Sandbox(modal.object._Provider[_SandboxHandle]):
    @staticmethod
    def _new(entrypoint_args: typing.List[str], image: modal.image._Image, mounts: typing.List[modal.mount._Mount]) -> _SandboxHandle:
        ...


class Sandbox(modal.object.Provider[SandboxHandle]):
    def __init__(self):
        ...

    @staticmethod
    def _new(entrypoint_args: typing.List[str], image: modal.image.Image, mounts: typing.List[modal.mount.Mount]) -> SandboxHandle:
        ...
