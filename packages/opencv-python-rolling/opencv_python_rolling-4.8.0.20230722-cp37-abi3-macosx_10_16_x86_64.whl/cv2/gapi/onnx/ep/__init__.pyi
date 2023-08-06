__all__: list[str] = []

import typing


# Classes
class OpenVINO:
    # Functions
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, device: str) -> None: ...

    def cfgDeviceType(self, type: str) -> OpenVINO: ...

    def cfgCacheDir(self, dir: str) -> OpenVINO: ...

    def cfgNumThreads(self, nthreads: int) -> OpenVINO: ...

    def cfgEnableOpenCLThrottling(self) -> OpenVINO: ...

    def cfgEnableDynamicShapes(self) -> OpenVINO: ...



